slug_result = 'Taken';
$('#slug').on('change', function (e) {
    e.preventDefault();
    checkUrl()
});

function checkUrl() {
    var slug = $('#slug').val();
    $.ajax({
        async: false,
        url: '/campaign/check/' + '?slug=' + slug,
        success: function (data) {
            if (data.result) {
                slug_result = 'Taken'
            } else {
                slug_result = 'Free'
            }
            $('#check_result').text(slug_result)
        }
    })
}