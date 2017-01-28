


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {


    setTimeout(function() {
        $(".twitter-icon").trigger('click');
    },10);

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

    $('.twitter-icon').click(function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        }
        $('.rep-action-container').css('display','block')
        $('.category-container').animate({'height':'350px'},400,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });

        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'},500,function() {})
        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').animate({'opacity':'0'});
        $('.twitter-icon-empty').animate({'opacity':'0'});
        $('.phone-icon').animate({'opacity':'0'});
        $('.email-icon').animate({'opacity':'0'});
        $('.twitter-name').animate({'opacity':'1.0'});
    });

    $('.twitter-icon-empty').click(function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        }

        $('.warning-box-tweet-icon').css({'opacity':'1'});
        $('.warning-box-tweet-icon').animate({'opacity':'0.0'},2500,function() {});
    });
    //alert("twitter clicked");

    $('.phone-icon').click( function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        alert("phone clicked");
    });

    $('.email-icon').click( function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        alert("email clicked");
    });

    $('#close-button').on('click',function(event) {
        if ($(':animated').length) {
            console.log("cancelling close button click");
            return false;
        }
        $('.category-container').animate({'height':'220px'});
        $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
            $('.rep-action-container').css('display','none')
        })
        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').animate({'opacity':'1'});
        $('.twitter-icon-empty').animate({'opacity':'1'});
        $('.phone-icon').animate({'opacity':'1'});
        $('.email-icon').animate({'opacity':'1'});
        $('.twitter-name').animate({'opacity':'0.0'});
    });


    $('#clear-button').on('click',function(event) {
        $('#text-input').val("");
    });

    $('#img-checked-box').on('click',function(event) {
        if ($(':animated').length) {
            console.log("cancelling click");
            return false;
        }
        //alert('The link is always included for context')
        $('.warning-box').css({'opacity':'1'});
        $('.warning-box').animate({'opacity':'0.0'},2500,function() {
        });
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
                "tweet_text": tweet_text,
                "segment_id": segment_id,
                "program_id": program_id,
                "last_menu_url": window_url
        });
         $.ajax({url: "/verify_twitter/",
                type: "POST",
                data: dataSet,
                contentType: 'json;charset=UTF-8',
                cache: false,
                success: function(data) {
                    // Success message
                    console.log('success');
                    window.location.href = data['redirectURL'];
                },
                error: function() {
                    // Fail message
                    console.log('fail :)');
                }
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