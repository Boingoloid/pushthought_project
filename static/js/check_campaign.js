slug_result = 'Taken';
$('#id_slug').keyup( function (e) {
    e.preventDefault();
    checkUrl()
});

function checkUrl() {
    var slug = $('#id_slug').val();
    var current = $("#current_slug").val();
    var slugged = slugify(slug);
    $('#id_slug').val(slugged);
    $.ajax({
        async: false,
        url: check_url + '?slug=' + slugged + '&current=' + current,
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
