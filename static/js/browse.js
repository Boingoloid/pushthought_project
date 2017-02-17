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


    $('.program-container').on('click','.program-item',function(event) {
        function showLoading(index){
            var loaderDiv = '.loader-' + index;
            console.log(loaderDiv);
            $(loaderDiv).show();
        }

        var idText = $(this).attr('id');
        var repIndex = idText.replace('program-item','');


        showLoading(repIndex);



        var programObjectIdElementName = "#program-item-objectId" + repIndex;
        var programId = $(programObjectIdElementName).text();
        // alert (programObjectId)
        window.location.href="/content_landing/" + programId;

//        var csrftoken = Cookies.get('csrftoken');
//        //var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();  //this also works
//        $.ajaxSetup({
//            beforeSend: function(xhr, settings) {
//                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                }
//            }
//        });

//
//       dataSet = JSON.stringify({
//                "programId": programId
//        });
//         $.ajax({url: "/content_landing/" + programId,
//                type: "GET",
////                data: dataSet,
////                contentType: 'application/json;charset=UTF-8',
////                cache: false,
//                success: function(data) {
//                    // Success message
////                    programId = data['programId']
////                    window.location.href='/content_landing/' + programId
//                },
//                error: function() {
//                    // Fail message
//                    console.log('fail :)')
//                },
//         });



    });


});



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