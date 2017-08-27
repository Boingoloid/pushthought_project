$(document).ready(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        checkUrl();
        if (slug_result === 'Taken') {
            alert('Push Thought URL is taken!');
            return false
        }

        var url = $('input[name=link]').val();
        if(url == ""){
            // do nothing, not required
        } else {

            url = validateUrl(url);
            if (!url) {
                alert("URL for 'Link to more information' has an error");
                return false
            }

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

function validateUrl(url) {
    var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    if (!re.test(url)) {
        return false;
    }
    return true
}