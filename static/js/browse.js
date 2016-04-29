$(document).ready(function() {

    // Browse Page
    $('.program-container').on('click','.program-item',function(event) {
       var idText = $(this).attr('id');
       var repIndex = idText.replace('program-item','');

       var programObjectIdTagName = "#program-item-objectId" + repIndex;
       var programObjectId = $(programObjectIdTagName).text();

       window.location.href="http://127.0.0.1:8000/program_detail/" + programObjectId;
    });

    // Back button on program_detail page
    $("#back-btn").on( "click", function() {
      window.location.href="http://127.0.0.1:8000/browse";
    });

    $('.segment-item-container').on('click','.segment-item',function(event) {
       var programObjectId = $("#program-objectId").text();

       var idText = $(this).attr('id');
       var segmentIndex = idText.replace('segment-item','');

       var segmentObjectIdTagName = "#segment-item-objectId" + segmentIndex;
       var segmentObjectId = $(segmentObjectIdTagName).text();

       window.location.href="http://127.0.0.1:8000/action_menu/" + programObjectId + "/" + segmentObjectId;
    });
});