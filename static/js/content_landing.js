$(document).ready(function() {

    $('.watch-button').click( function() {
//       var idText = $(this).attr('id');
//       var repIndex = idText.replace('program-item','');
//
//       var programObjectIdElementName = "#program-item-objectId" + repIndex;
//       var programObjectId = $(programObjectIdElementName).text();

       window.location.href="/leaving";
    });

    $('.twitter-icon').click( function() {
        $('.rep-container').css('height','700px');
        alert("twitter clicked");
    });

    $('.phone-icon').click( function() {
        alert("phone clicked");
    });

    $('.email-icon').click( function() {
        alert("email clicked");
    });

    $('.tweet-container').on('click','.tweet-item',function(event) {
       var idText = $(this).attr('id');
       var tweetIndex = idText.replace('tweet-item','');

       var tweetObjectIdElementName = "#tweet-item-objectId" + tweetIndex;
       var tweetObjectId = $(programObjectIdElementName).text();
       window.location.href="/content_landing/" + tweetObjectId;
    });

});