$(document).ready(function () {
    $('#search_btn').on('click', function () {
        var text_in_search = String($('#search_keyword').val());


        if(text_in_search == ''){

            alert("you must enter a link to IMDB or YouTube");
            console.log("not validated");
            return false;
        }


        var validation = text_in_search.match(/(youtube.com|imdb.com)/);

        if(validation){
            let imdb_url = $('#search_keyword').val();
            let url = `${imdb_id_search_url}?q=${imdb_url}`;
            window.location.href = url;

        } else{
            alert("link must be from IMDB (internet movie database) or YouTube")
        }
    });
});