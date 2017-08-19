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
            console.log("returning false");
            return false;
        }


        var message = $(this).val();

        if($('.rep-action-container').is(":visible")){
        }else{
            $('.email-icon').trigger('click');
        }

        ////////// append message in input after span node

        $('.address-placeholder').after(message);
        $('.address-placeholder').remove();
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


});

