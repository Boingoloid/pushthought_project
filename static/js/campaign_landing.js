$(document).ready(function() {



    // Facebook and Twitter sharing buttons
    var current_url = window.location.href;
    var fb_text = $("p.description").text().length ? $("p.description").text() : 'I just contacted my congressional reps on Push Thought'
    params = {
      'text': 'I just contacted my congressional reps on Push Thought',
      'url': current_url
    }
    $("#twitter-share-button").prop('href', "https://twitter.com/intent/tweet?"+$.param(params));

    $("#facebook-share-button").click(function(){
      FB.ui({
        method: 'share',
        href: current_url,
        quote: fb_text,
      }, function(response){});
    });
});
