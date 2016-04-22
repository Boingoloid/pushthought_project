$(document).ready(function() {
    $('.program-container').on('click','.program-item',function(event) {
       var idText = $(this).attr('id');
       var repIndex = idText.replace('program-item','');


       var programObjectIdTagName = "#program-item-objectId" + repIndex;
       var programObjectId = $(programObjectIdTagName).text();


       window.location.href="http://127.0.0.1:8000/program_detail/" + programObjectId;


    });
});