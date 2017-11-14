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
        address = address.replace('@','');
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
        var tweet_text = $('#text-input').text() + site_url_to_append;
        console.log("tweet text:", tweet_text );
        console.log("html:", $('#text-input').html());
        if(tweet_text.length < 1){
            alert ("Please type a message first");
            return false;
        } else if ($('.letter-count').text() < 0){
            alert ("Your tweet is too long, please edit to reduce character count");
            return false;
        }

        showLoadingForSelectedMembers();

         // Get program and segment Id
         var programId = $('#programId').text();
         var campaignId = $('#campaignId').text();
         var segmentId = $('#segmentId').text();

        // Build Address Array.
        var addressArray = [];
        $('.address-item.selected').each(function(){
            var address = $(this).text();
            address = address.replace(/\n/g,'').slice(1);
            addressArray.push(address);
        });
        console.log("address array", addressArray);


        // create dataSet string
        var dataSet = {
            "tweet_text": tweet_text,
            "segment_id": segmentId,
            "program_id": programId,
            "campaign_id": campaignId,
            "last_menu_url": windowURL,
            "address_array" : addressArray,
        };
        console.log("dataset: ",dataSet);


        return $.ajax({url: "/verify_catch/",
            type: "POST",
            data: dataSet,
            cache: false,
            traditional: true,
            success: function(data) {
                hideLoading();
                show_status(data);
            },
            error: function(xhr, textStatus, error) {
                hideLoading();
                if (xhr.status == 404) {
                    alert("This account doesn't have a twitter account binded to it.")
                }
            }
        });
    }
}
