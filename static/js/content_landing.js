


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



$(document).ready(function() {

    var csrftoken = Cookies.get('csrftoken');
    //var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();  //this also works
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $('.watch-button').click( function() {
       //var idText = $(this).attr('id');
       //var repIndex = idText.replace('program-item','');
       //var programObjectIdElementName = "#program-item-objectId" + repIndex;
       //var programObjectId = $(programObjectIdElementName).text();
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
    var segment_id = $('#segmentId').text();
    var program_id = $('#programId').text();

    $('#tweet-button').on('click',function(event) {

      var tweet_text = $('#text-input').val();

      if(tweet_text.length < 1){
        alert ("Please type a message to tweet first");
      } else {
        dataSet = JSON.stringify({
            data: {
                "tweet_text": tweet_text,
                "segment_id": segment_id,
                "program_id": program_id,
                "last_menu_url": window_url
            }
        });
         $.ajax({url: "/verify_twitter",
                type: "POST",
                data: dataSet,
                contentType: 'application/json;charset=UTF-8',
                cache: false,
                success: function(data) {
                    // Success message
                    console.log('success')
                    window.location.href = data['redirect_url'];

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

//        window.location.href = window_url;

//        Create and encode URL
//        var encodedTweetText = encodeURIComponent(tweetText);
});