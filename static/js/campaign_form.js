$(document).ready(function() {

    updateLetterCount();

    $('.field-input-tweet_text').keyup(function() {
        console.log("keyup function");
        updateLetterCount();
    });

    //***********************************************
    // This JavaScript validation section does not appear to be necessary -Ben
    //**************************************************

    // $("#id_slug").blur(function(){
    //   checkUrl();
    //   if (slug_result === 'Taken') {
    //       alert('url taken!');
    //   }
    // })

    // var url = $('input[name=link]').val();
    // var validated_url = validateUrl(url);
    // if (url.length >0 && !validated_url) {
    //     alert("URL for 'Link to more information' has an error");
    //     return false
    // }

    // $('.field-input-url').on('click', function(e) {
    //     if($('#submit').text() == "SAVE CHANGES"){
    //         alert("Push Thought URL field cannot be changed after it is created.");
    //     }
    // });

    // $('#campaign-form').on('submit', function(e) {
        // e.preventDefault();
        // checkUrl();
        // if (slug_result === 'Taken') {
        //     alert('url taken!');
        // }
    //
    //     var url = $('input[name=link]').val();
    //     var validated_url = validateUrl(url);
    //     if (url.length >0 && !validated_url) {
    //         alert("URL for 'Link to more information' has an error");
    //         return false
    //     }
    //     return true;
        // Perform validation


        // if($('textarea[name=tweet_text]').val() || $('textarea[name=email_text]').val()) {
        //
        //     error = false;
        // } else {
        //     alert('Please fill up one field');
        //     error = true;
        // }

        // Check error flag before submission
        // if(!error) {
        //     return true
        // } else {
        //     return false
        // }
    // });

});

// This function appears to be unnecessary
function validateUrl(url) {
    var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    if (!re.test(url)) {
        return false;
    }
    return true
}

function updateLetterCount(){
    console.log("here");
    var twitterMax = 140;
    var twitterDefaultNameLength = 20;
    var countAfterName = twitterMax - twitterDefaultNameLength;
    var textInput = $('.field-input-tweet_text')
    var characterCount = textInput.val().length;
    console.log("char count", characterCount);
    numberOfLineBreaks = (textInput.text().match(/\n/g)||([])).length;
    console.log("line breaks", numberOfLineBreaks);
    var letterCount = countAfterName - characterCount - numberOfLineBreaks;
    $('.tweet-letter-count').text(letterCount);
    console.log("now here");
}
