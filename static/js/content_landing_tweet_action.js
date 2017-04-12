




function runTweet(windowURL){
    // get message length and validate length
    var tweet_text = $('#text-input').text();
    if(tweet_text.length < 1){
        alert ("Please type a message first");
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
     var segmentId = $('#segmentId').text();

    // Build Address and Bioguide Array
    var addressArray = [];
    var bioguideArray = [];
    $('.address-item.selected').each(function(){
        var address = $(this).text();
        address = address.replace('\n','');
        address = address.replace('\n','');
        address = address.replace('\n','');
        addressArray.push(address);
        var bioguideId = $(this).attr('name');
        console.log(bioguideId);
        bioguideArray.push(bioguideId);
    });
    console.log("address array", addressArray);
    console.log("bioguide array", bioguideArray);


    // create dataSet string
    var dataSet = JSON.stringify({
            "tweet_text": tweet_text,
            "segment_id": segmentId,
            "program_id": programId,
            "last_menu_url": windowURL,
            "bioguide_array" : bioguideArray,
            "address_array" : addressArray,
    });
    console.log(dataSet);

    $.ajax({url: "/verify_twitter/",
        type: "POST",
        data: dataSet,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {

            // Success message
            console.log('success, here is the data:'+ data);


            if(data['redirectURL']){
                 window.location.href = data['redirectURL'];
            }else if(data['overMax']){
                alert("Tweet is over 140 characters. Shorten a few characters and try again.");
                hideLoading();
                $('#text-input').focus();
                setEndOfContenteditable($('#text-input'));
            }else if(data['success']){
                hideLoading();
                alert("Your tweet has been sent.");
                $('.close').trigger('click');
            }else if(data['duplicate']){
                hideLoading();
                alert("Message is duplicate on your twitter account.  Please alter your message and try again.");
            }else if(data['other']){
                hideLoading();
                alert("There has been an error with twitter.  Please check message and try again.  If it persists, notify Push Thought");
            } else {
                var len = data['successArray'].length;
                if(data['successArray'].length !=0){
                    successArray = data['successArray'];
                } else {
                    successArray = [];
                }

                if(data['duplicateArray'].length !=0){
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
        error: function() {
            $('.loader').hide();
            // Fail message
            console.log('fail :)');
        }
    });
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

// loop through and find longest address
function get_longest_address(){
    var longestAddressLength = 0;
    $('.address-item-label:visible').each(function(){
        var text = $(this).text();
        if (text.length > longestAddressLength){
            longestAddressLength = text.length;
        }
    });
    return longestAddressLength;
}