


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {


//    setTimeout(function() {
//        $(".twitter-icon").trigger('click');
//    },10);

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
        };
        $('.rep-action-container').css('display','block'),200,function(){
            //var caretPos = $("#text-input").selectionStart;
            //var textAreaTxt = $("#text-input").val();
            //var txtToAdd = "stuff";
            //$("#text-input").val(textAreaTxt.substring(0, caretPos) + txtToAdd + textAreaTxt.substring(caretPos));
        };
        $('.category-container').animate({'height':'350px'},200,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'},500,function() {
                console.log($("#text-input").val())
                $("#text-input").val("@ multiple")
            })

        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').animate({'opacity':'0'});
        $('.twitter-icon').css('display','none')
        $('.twitter-icon-empty').animate({'opacity':'0'});
        $('.twitter-icon-empty').css('display','none')
        $('.phone-icon').animate({'opacity':'0'});
        $('.phone-icon').css('display','none')
        $('.email-icon').animate({'opacity':'0'});
        $('.email-icon').css('display','none')
        $('.twitter-name').animate({'opacity':'1.0'},400,function(){
        });
        $(this).parent('div').parent('div').toggleClass("selected");

        var index = $(this).parent('div').parent('div').attr('id');
        console.log(index);
        var addressPath = ".address-item-" + index;
        console.log(addressPath);
        $(addressPath).toggleClass('selected');

        addressPlaceholderClass= '.address-label-' + index;
        addressPlaceholder = $(addressPlaceholderClass).html()
        $('#text-input').html('<span class=address-placeholder>' + addressPlaceholder + '</span>');
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
        $('.twitter-icon').show()
        $('.twitter-icon-empty').animate({'opacity':'1'});
        $('.twitter-icon-empty').show();
        $('.phone-icon').animate({'opacity':'1'});
        $('.phone-icon').show();
        $('.email-icon').animate({'opacity':'1'});
        $('.email-icon').show();
        $('.twitter-name').animate({'opacity':'0.0'});
        $('.rep-color-band').animate({'height':'233px'});
        $('.selected').animate($('.selected').removeClass('selected'));
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

    var textStart = '';
    var textEnd = '';
    var placeholderText = '';


    $('#text-input').keydown(function() {
        textStart = $(this).html();
        console.log(textStart);
        var numItems = $('.address-item.selected').length;
        if (numItems == 1){
            placeholderText = $('.address-item.selected').children('p').html();
        } else {
            placeholderText = '@multiple';
        }
    });

    $('#text-input').keyup(function() {
        textEnd = $(this).text();
        console.log('output');
        console.log('textecd:' + textEnd);
        console.log("placeholder" + placeholderText);
        if (textEnd.indexOf(placeholderText) > -1){
            return false;
        } else {
            alert("This is where will put the twitter names.  Add text before and after.");
            $(this).html(textStart);
            textStart = '';
            textEnd = '';
            placeholderText = '';
        }
    });


    $('.action-panel-container').on('click', function(){
        if($('.twitter-name').css('opacity') == 0) {
            return false
        } else {
            if ($(this).hasClass( "selected" )){
                $(this).removeClass('selected');

                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-item-" + index;
                $(addressPath).removeClass('selected');

            } else {
                $(this).addClass('selected');

                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-item-" + index;
                $(addressPath).addClass('selected');
            }

            var numItems = $('.address-item.selected').length;
            if (numItems == 1){
                placeholderText = $('.address-item.selected').children('p').html();
                $('.address-placeholder').text(placeholderText);
            } else {
                placeholderText = '@multiple';
                $('.address-placeholder').text('@multiple');
            }

        }



    });

    function updatePlaceholder(){
        var numItems = $('.address-item.selected').length;
        console.log(numItems);
    }


//    // CLICK ACTIONS
//    $('.rep-container').on('click','.rep-item',function(event) {
//        // extract index # of click and grab twitter address
//       var idText = $(this).attr('id');
//       var repIndex = idText.replace('rep-item','');
//       var tweetAddressID = "#tweet-address-item" + repIndex;
//       var tweetAddress = $(tweetAddressID).text();
//       var currentText = $('#text-input').val();
//
//
//       if ($(this).css('background-color') === 'rgb(255, 255, 255)'){
//
//         $(this).css('background-color','green');
//         currentText += tweetAddress;
//         $('#text-input').val(currentText);
//
//       } else {
//
//        $(this).css('background-color','white');
//        var n = currentText.search(tweetAddress);
//        //console.log(n);
//        var re = new RegExp(tweetAddress,"gi");
//        var newText = currentText.replace(re,"");
//        $('#text-input').val(newText);
//       }
//    });

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