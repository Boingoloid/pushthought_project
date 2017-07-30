$(document).ready(function () {
    // $('#search_keyword').on('keyup', function () {
    //     let q = $(this).val();
    //     $.ajax({
    //         url: imdb_id_search_url + '?q=' + q,
    //         success: function (data) {
    //
    //         }
    //     })
    // })

    $('#search_btn').on('click', function () {
        let imdb_url = $('#search_keyword').val();
        let url = `${imdb_id_search_url}?q=${imdb_url}`;
        window.location.href = url
    })
});