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
        var text_in_search = String($('#search_keyword').val());


        if(text_in_search == ''){

            alert("you must enter a link to IMDB or YouTube");
            console.log("not validated");
            return false;
        }


        var validation = false;

        var youtube_https = text_in_search.substring(0, 23);
        var youtube_www = text_in_search.substring(0, 15);
        console.log('youtube_https: '+ youtube_https);
        console.log("youtube_www: " + youtube_www);

        if(youtube_https == "https://www.youtube.com" || youtube_www == "www.youtube.com"){
            validation = true;
            console.log("youtube validated");
        }

        var imdb_https = text_in_search.substring(0, 19);
        var imdb_www = text_in_search.substring(0, 12);

        console.log("imdb_https: " + imdb_https);
        console.log("imdb_www: " + imdb_www);

        if(imdb_https == "http://www.imdb.com" ||   imdb_www == "www.imdb.com"){

            validation = true;
            console.log("imdb validated");

        }

        if(validation){
            alert("Success!")
            let imdb_url = $('#search_keyword').val();
            let url = `${imdb_id_search_url}?q=${imdb_url}`;
            window.location.href = url;

        } else{
            alert("link must be from IMDB (internet movie database) or YouTube")
        }
    });
});