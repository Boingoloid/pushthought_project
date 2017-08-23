$(document).ready(function() {


//    jQuery(function ($) {
//        var $textareas = $('textarea[name=field-input-tweet-text],textarea[name=field-input-email-text]');
//        $textareas.on('textarea', function () {
//            // Set the required property of the other input to false if this input is not empty.
//            $textareas.not(this).prop('required', !$(this).val().length);
//        });
//    });


        $('form').on('submit', function(e) {
            e.preventDefault();
            checkUrl();
            if (slug_result === 'Taken') {
                alert('url taken!');
                return false
            }

            // Perform validation
            var error = false;

            if($('textarea[name=tweet_text]').val() || $('textarea[name=email_text]').val()) {
                alert('Passed validation');
                error = false;
            } else {
                alert('Please fill up one field');
                error = true;
            }

            // Check error flag before submission
            if(!error) $(this)[0].submit();
        });



});