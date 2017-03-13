




function runTweet(){
    // get message length and validate length
    var tweet_text = $('#text-input').text();
    if(tweet_text.length < 1){
        alert ("Please type a message first");
        return false;
    }
    addressArray = [];
    $('.action-panel-container.selected').each(function() {
        index = $(this).attr('id');
        function showLoading(index){
            var loaderDiv = '.loader-' + index;
            $(loaderDiv).show();
            $('.tweet-loader').show();
        }
        showLoading(index);

        twitterName = $(this).contents().contents('.twitter-name').text();
        addressArray.push(twitterName);
     });
    // create dataSet string
    var dataSet = JSON.stringify({
            "tweet_text": tweet_text,
            "segment_id": segment_id,
            "program_id": program_id,
            "last_menu_url": window_url,
            "address_array" : addressArray,
    });
    console.log(dataSet);

    $.ajax({url: "/verify_twitter",
        type: "POST",
        data: dataSet,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {

            // Success message
            console.log('success, here is the data:'+ data);


            if(data['redirectURL']){
                 window.location.href = data['redirectURL'];
            } else {
                var len = data['successArray'].length;
//                    console.log(data['successArray'].length);
//                    console.log(data['duplicateArray'].length);
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

                function hideLoading(){
                    $('.loader').hide();
                    $('.tweet-loader').hide();
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