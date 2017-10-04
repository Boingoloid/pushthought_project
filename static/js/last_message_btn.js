$('.copy-last').on('click', function () {
    var html = $('#text-input').html();
    var last_message = $('#last-message').text().split(',').slice(1).join().slice(1);
    $('#text-input').html(html + last_message)
});