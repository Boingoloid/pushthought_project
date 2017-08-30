function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function() {



    $('.browse-button-a').hover( function () {
        console.log("hello");
        var acc = $('.accordion');
        if ($('.panel').css('opacity') == 0){
            $(".panel").css("opacity", "1.0");
            $(".panel").css("height", "auto");
            $(".panel").css("border-top", "3px solid white");
            console.log("make appear");
        } else {
            $(".panel").css("opacity", "0.0");
            $(".panel").css("height", "0");
            $(".panel").css("border-top", "0px solid white");
            console.log("make disappear");
        }
    });

    /////////////////////////////////////////////
    // toggle button click on campaigns
    ////////////////////////////////////////////
    $('.campaigns-button').on('click', function(e){

        $('.campaigns-button').addClass('selected');
        $('.campaigns-button').css('background-color','green');
        $('.campaigns-button').css('color','black');

        $('.content-button').removeClass('selected');
        $('.content-button').css('background-color','#337ab7');
        $('.content-button').css('color','white');
    });


    /////////////////////////////////////////////
    // toggle button click on content
    ////////////////////////////////////////////
    $('.content-button').on('click', function(e){

        $('.content-button').addClass('selected');
        $('.content-button').css('background-color','green');
        $('.content-button').css('color','black');

        $('.campaigns-button').removeClass('selected');
        $('.campaigns-button').css('background-color','#337ab7');
        $('.campaigns-button').css('color','white');

    });

    /////////////////////////////////////////////
    // by default, trigger campaigns toggle button
    ////////////////////////////////////////////
    $('.campaigns-button').trigger('click');



});

    // $("#search_btn").click(function(){
    //     alert("search feature under development");
    //     // $("#search_type").val("scraping");
    //     // console.log($("#search_type").val());
    //     // $("form").submit();
    // });

    // $('.program-container').on('click','.program-item',function(event) {
    //     $(this).contents('#loader').show();
    //     var programId = $(this).attr('id');
    //     window.location.href="/content_landing/" + programId;
    // });

//    $('.segment-item-container').on('click','.segment-item',function(event) {
//       var programObjectId = $("#program-objectId").text();
//
//       var idText = $(this).attr('id');
//       var segmentIndex = idText.replace('segment-item','');
//
//       var segmentObjectIdTagName = "#segment-item-objectId" + segmentIndex;
//       var segmentObjectId = $(segmentObjectIdTagName).text();
//
//       window.location.href="http://127.0.0.1:8000/action_menu/" + programObjectId + "/" + segmentObjectId;
//    });



//    var acc = $('.accordion');
//    var i;
//
//    for (i = 0; i < acc.length; i++) {
//      acc[i].onmouseover = function() {
//        this.classList.toggle("active");
//        var panel = this.nextElementSibling;
//        if (panel.style.maxHeight){
//          panel.style.maxHeight = null;
//        } else {
//          panel.style.maxHeight = panel.scrollHeight + 'px';
//        }
//      }
//
//      acc[i].onmouseout = function() {
//        this.classList.toggle("active");
//        var panel = this.nextElementSibling;
//        if (panel.style.maxHeight){
//          panel.style.maxHeight = null;
//        } else {
//          panel.style.maxHeight = panel.scrollHeight + 'px';
//        }
//      }
//    }