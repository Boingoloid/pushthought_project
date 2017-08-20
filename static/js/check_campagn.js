$('#check_url').on('click', function (e) {
    e.preventDefault();
    var slug = $('#slug').val();
    $.ajax({
        url: '/campaign/check/' + '?slug=' + slug,
        success: function (data) {
            var result;
            if (data.result) {
                result = 'Taken'
            } else {
                result = 'Free'
            }
            $('#check_result').text(result)
        }
    })
});