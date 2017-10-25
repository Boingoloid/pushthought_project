var twitter_url = '';
$(document).ready(function () {
    $(document).on('change', '#twitter_input_add_url', function () {
        if ($(this).prop('checked')) {
            twitter_url = ' pushthought.com/' + window.location.href.split('/').slice(3).join('/');
        } else {
            twitter_url = ''
        }
        updateTextCount()
    })
});