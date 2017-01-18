function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {



    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//    csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.watch-button').click( function() {
//       var idText = $(this).attr('id');
//       var repIndex = idText.replace('program-item','');
//
//       var programObjectIdElementName = "#program-item-objectId" + repIndex;
//       var programObjectId = $(programObjectIdElementName).text();

       window.location.href="/leaving";
    });

    $('.twitter-icon').click( function() {
        $('.rep-container').css('height','700px');
        alert("twitter clicked");
    });

    $('.phone-icon').click( function() {
        alert("phone clicked");
    });

    $('.email-icon').click( function() {
        alert("email clicked");
    });

    $('#clear-button').on('click',function(event) {
        $('#text-input').val("");
    });

    $('.img-checked-box').on('click',function(event) {
        alert('The link is always included for context')
    });


    var window_url =  window.location.href;
    var segmentId = $('#segmentId').text();
    //    "JPGM9mmcKV";
    var programId = $('#programId').text();
    //alert (segmentId);

    $('#tweet-button').on('click',function(event) {

      var tweet_text = $('#text-input').val();

      if(tweet_text.length < 1){
        alert ("Please type a message to tweet first");
      } else {
        alert (tweet_text);
        //Create and encode URL
        //var encodedTweetText = encodeURIComponent(tweetText);
        //window_url = "http://127.0.0.1:8000";
        //window_url += "/verify_twitter/" + programId + "/" + segmentId;
        //window_url += "/" + encodedTweetText;

        var twitter_username = "username"
        var twitter_password = "password"
        // For Success/Failure Message
        // Check for white space in name for Success/Fail message

        dataSet = JSON.stringify({
            data: {
                tweet_text: tweet_text,
                twitter_username: twitter_username,
                twitter_password: twitter_password
            }
        });

         $.ajax({url: "/verify_twitter",
                type: "POST",
                data: dataSet,
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                success: function() {
                    // Success message
                    console.log('success')
                },
                error: function() {
                    // Fail message
                    console.log('fail :)')
                },
            });

      }
    });


//    $('.tweet-container').on('click','.tweet-item',function(event) {
//       var idText = $(this).attr('id');
//       var tweetIndex = idText.replace('tweet-item','');
//
//       var tweetObjectIdElementName = "#tweet-item-objectId" + tweetIndex;
//       var tweetObjectId = $(programObjectIdElementName).text();
//       window.location.href="/content_landing/" + tweetObjectId;
//    });

});