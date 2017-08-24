slug_result = 'Taken';
$('#slug').on('change', function (e) {
    e.preventDefault();
    checkUrl()
});

function checkUrl() {
    var slug = $('#slug').val();
    var slugged = slugify(slug);
    $('#slug').val(slugged);
    $.ajax({
        async: false,
        url: '/campaign/check/' + '?slug=' + slugged,
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

function slugify(text)
{
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
}