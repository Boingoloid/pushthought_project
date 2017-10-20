var login_url;
function check_user() {
    return $.ajax({
        url: "/is_logged_in/",
        async: false,
        success: function(data) {
            console.log('Logged in:');
            console.log(data);
            login_url = data
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function login_user(url) {
    var addressArray = [];
     $('.address-item.selected').each(function(){
        var address = $(this).text();
        address = address.replace('\n','');
        address = address.replace('\n','');
        address = address.replace('\n','');
        addressArray.push(address);
    });

    var tweetForm = document.createElement("form");
    tweetForm.method = "POST"; // or "post" if appropriate
    tweetForm.action = url

    var tweetInput = document.createElement("input");
    tweetInput.type = "text";
    tweetInput.name = "tweet_text";
    tweetInput.value = $('#text-input').text();
    tweetForm.appendChild(tweetInput);

    var program_idInput = document.createElement("input");
    program_idInput.type = "text";
    program_idInput.name = "program_id";
    program_idInput.value = $('#programId').text();
    tweetForm.appendChild(program_idInput);

    var campaign_idInput = document.createElement("input");
    campaign_idInput.type = "text";
    campaign_idInput.name = "campaign_id";
    campaign_idInput.value = $('#campaignId').text();
    tweetForm.appendChild(campaign_idInput);

    var address_arrayInput = document.createElement("input");
    address_arrayInput.type = "text";
    address_arrayInput.name = "address_array";
    address_arrayInput.value = addressArray;
    tweetForm.appendChild(address_arrayInput);

    var tokenInput = document.createElement("input");
    tokenInput.type = "text";
    tokenInput.name = "csrfmiddlewaretoken";
    tokenInput.value = csrftoken;
    tweetForm.appendChild(tokenInput);

    document.body.appendChild(tweetForm);
    tweetForm.submit();
}

function runTweet(windowURL){
    var login_window;
    check_user();
    if (login_url) {
        login_user(login_url)
    } else {
        // get message length and validate length
        var tweet_text = $('#text-input').text();
        console.log("tweet text:", tweet_text );
        console.log("html:", $('#text-input').html());
        if(tweet_text.length < 1){
            alert ("Please type a message first");
            return false;
        } else if ($('.letter-count').text() < 0){
            alert ("Your tweet is too long, please edit to reduce character count");
            return false;
        }


        // Show loaders
        $('.action-panel-container.selected').each(function() {
            index = $(this).attr('id');
            function showLoading(index){
                var loaderDiv = '.loader-' + index;
                $(loaderDiv).show();
                $('.tweet-loader').show();
            }
            showLoading(index);
         });


         // Get program and segment Id
         var programId = $('#programId').text();
         var campaignId = $('#campaignId').text();
         var segmentId = $('#segmentId').text();

        // Build Address and Bioguide Array
        var addressArray = '';
        var bioguideArray = '';
        $('.address-item.selected').each(function(){
            var address = $(this).text();
            address = address.replace('\n','');
            address = address.replace('\n','');
            address = address.replace('\n','');
            addressArray += ', ' + address;
            var bioguideId = $(this).attr('name');
            console.log(bioguideId);
            bioguideArray += ', ' + bioguideId;
        });
        console.log("address array", addressArray);
        console.log("bioguide array", bioguideArray);


        // create dataSet string
        var dataSet = {
                "tweet_text": tweet_text,
                "segment_id": segmentId,
                "program_id": programId,
                "campaign_id": campaignId,
                "last_menu_url": windowURL,
                "bioguide_array" : bioguideArray,
                "address_array" : addressArray,
        };
        console.log("dataset: ",dataSet);


        $.ajax({url: "/verify_catch/",
            type: "POST",
            data: dataSet,
            cache: false,
            success: function(data) {

                // Success message
                console.log('success, here is the data:'+ data);


                if(data.status == 'overMax') {
                    alert("Tweet is over 140 characters. Shorten a few characters and try again.");
                    hideLoading();
                    $('#text-input').focus();
                    setEndOfContenteditable($('#text-input'));
                } else if(data.status == 'noMention'){
                    alert("No receiver found.");
                    hideLoading();
                    $('#text-input').focus();
                    setEndOfContenteditable($('#text-input'));
                }else if(data.status == 'success'){
                    hideLoading();
                    alert("Your tweet has been sent.");
                    $('.close').trigger('click');
                }else if(data.status == 'duplicate'){
                    hideLoading();
                    alert("Message is duplicate on your twitter account.  Please alter your message and try again.");
                }else if(data.status == 'other'){
                    hideLoading();
                    alert("There has been an error with twitter.  Please check message and try again.  If it persists, notify Push Thought");
                } else {
                    var len = data['successArray'].length;
                    if(data.successArray.length !=0){
                        successArray = data['successArray'];
                    } else {
                        successArray = [];
                    }

                    if(data.duplicateArray.length !=0){
                        duplicateArray = data['duplicateArray'];
                    } else {
                        duplicateArray = [];
                    }


                    if (successArray.length > 0){
                        $.when(hideLoading()).then(showSuccess(successArray, duplicateArray)).then($('#close-button').trigger('click'));
                        //showSuccess(successArray, duplicateArray);
                    } else {
                        $.when(hideLoading()).then(showSuccess(successArray, duplicateArray));
                    }
                }
            },
            error: function(xhr, textStatus, error) {
                $('.loader').hide();
                $('.tweet-loader').hide();
                // Fail message
                if (xhr.status == 404) {
                    alert("This account doesn't have a twitter account binded to it.")
                }

                console.log('fail :)');
            }
        });
    }
}

// hide loading
function hideLoading(){
    $('.loader').hide();
    $('.tweet-loader').hide();
}

function moveCursorToEnd(element){
    element.focus();
    var val = element.html();
    console.log(val);
    element.html('');
    console.log(element.html());
    element.html(val);
    console.log(element.html());
}


function setEndOfContenteditable(contentEditableElement)
{
    var range,selection;
    if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
    {
        range = document.createRange();//Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(contentEditableElement[0]);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection();//get the selection object (allows you to change selection)
        selection.removeAllRanges();//remove any selections already made
        selection.addRange(range);//make the range you have just created the visible selection
    }
    else if(document.selection)//IE 8 and lower
    {
        range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
        range.moveToElementText(contentEditableElement[0]);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        range.select();//Select the range (make it the visible selection
    }
}
