$(document).ready(function() {

    $('.tweet_suggested_message_container').on("click", ".field-suggested-tweet", function(e) {
        e.stopPropagation();

        var message = $(this).val();

        if($('.rep-action-container').is(":visible")){
        }else{
            $('.twitter-icon').trigger('click');
        }

        pasteMessage(message);

    });

    $('.email_suggested_message_container').on("click", ".field-suggested-email", function(e) {
        e.stopPropagation();
        console.log($('.tweet-button-label').text().slice( 0, 5 ));

        var sliced_string = $('.tweet-button-label').slice( 0, 5 )
        sstring = String(sliced_string);

        if($('.rep-action-container').is(":visible") && $('.tweet-button-label').slice( 0, 5 ) == sstring){
            alert("Sorry, you can't paste email text into a tweet.");
            return false;
        }


        var message = $(this).val();

        if($('.rep-action-container').is(":visible")){
        }else{
            $('.email-icon').trigger('click');
        }

        ////////// append message in input after span node

        $('.address-placeholder').after('\n'+message);

        //$('.address-placeholder').remove();
    });

    function pasteMessage(message){
        ////////// grab placeholder text
        placeholder_text = $('.address-placeholder').text();

        ////////// reinsert black placeholder span
        $('#text-input').html("<span contenteditable='false' class='address-placeholder'></span>");

        ////////// reinsert placeholder text in span
        $('.address-placeholder').text(placeholder_text);

        ////////// append message in input after span node
        $('.address-placeholder').after(message);

    }

    // Facebook and Twitter sharing buttons
    var current_url = window.location.href;
    var fb_text = $("p.description").text().length ? $("p.description").text() : 'I just contacted my congressional reps on Push Thought'
    params = {
      'text': 'I just contacted my congressional reps on Push Thought',
      'url': current_url
    }
    $("#twitter-share-button").prop('href', "https://twitter.com/intent/tweet?"+$.param(params));

    $("#facebook-share-button").click(function(){
      FB.ui({
        method: 'share',
        href: current_url,
        quote: fb_text,
      }, function(response){});
    });
});
