$(document).ready(function() {
    $('#submit').on('submit', function(e) {
        e.preventDefault();
        checkUrl();
        if (slug_result === 'Taken') {
            alert('url taken!');
            return false
        }

        var url = $('input[name=link]').val();
        var validated_url = validateUrl(url);
        if (url.length >0 && !validated_url) {
            alert("URL for 'Link to more information' has an error");
            return false
        }

        // Perform validation
        var error = false;

        if($('textarea[name=tweet_text]').val() || $('textarea[name=email_text]').val()) {

            error = false;
        } else {
            alert('Please fill up one field');
            error = true;
        }

        // Check error flag before submission
        if(!error) {
            return true
        } else {
            return false
        }
    });
});

function validateUrl(url) {
    var re = /^(http[s]?:\/\/){0,1}(www\.){0,1}[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,5}[\.]{0,1}/;
    if (!re.test(url)) {
        return false;
    }
    return true
}
