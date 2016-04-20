$(document).ready(function() {

    var window_url =  window.location.href;

    Parse.initialize("lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM", "tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP");
    Parse.serverURL = 'https://ptparse.herokuapp.com/parse';

    // DECLARING VARIABLES FOR FETCHED DATA
    var programData = JSON.parse($("#programData").text());
    var segmentData = JSON.parse($("#segmentData").text());
    var programId = $("#programId").text();    //"JvW9oAYlo8";
    var segmentId = $("#segmentId").text();     // "JPGM9mmcKV";
    var segmentTitle = segmentData['segmentTitle'];


//    var SegmentIdentifier = $("#segmentId").text();
//    if(segmentId == SegmentIdentifier){
//        console.log("yes the segmentIds are the same! (top clickhandlers)");
//    } else {
//        console.log("no the segmentIds are NOT the same! (top clickhandlers)");
//    }



    $('.action-container').on('click','.action-item',function(event) {
        var selectedCategory = $(this).html();
        console.log(selectedCategory);

        var menuDataFiltered = _.filter(menuData, function(item){
           return item.get('actionCategory') == selectedCategory;
        });

        if(selectedCategory == "Local Representative"){
            window.location.href="http://127.0.0.1:8000/action_menu/JvW9oAYlo8/JPGM9mmcKV/fed_representative.com";
        } else if(selectedCategory == "Petition") {
            window.location.href="http://127.0.0.1:8000/action_menu/JvW9oAYlo8/JPGM9mmcKV/petition.com";
        } else {
            window.location.href="www.google.com";
        }
    });
});



      // GET SEGMENT & Program info and update HTML
      //getSegmentData(segmentId,programId);


//        // GET MENU LIST DATA
//      var MessageList = Parse.Object.extend("Messages");
//      var query = new Parse.Query(MessageList);
//      query.equalTo("segmentId", segmentId);
//      query.find({
//          success: function(results) {
//
//            // SORTING THE MESSAGE RESULTS
//            var SortedResults = results.sort(function(a, b){
//              var nA = a.get('actionCategory');
//              var nB = b.get('actionCategory');
//              if(nA < nB)
//                return -1;
//              else if(nA > nB)
//                return 1;
//              return 0;
//            });
//
//            // ASSIGN SORTED RESULTS TO VARIABLE - ACCESSED ON SELECTION OF CATEGORY
//            menuData = SortedResults;
//
//            // GET UNIQUE VALUES FOR ACTION MENU
//            var uniqueResults = _.unique(SortedResults, false, function(item){
//              return item.get('actionCategory');
//            });
//
//            // BRING LOCAL REP TO FRONT
//            $.each(uniqueResults,function(i,result){
//                if(result.get('actionCategory') == "Petition"){
//                    //move to first
//                    uniqueResults.unshift(result);
//                    uniqueResults.splice(i+1, 1);
//                }
//            });
//
//            // BRING REGULATOR TO FRONT
//            $.each(uniqueResults,function(i,result){
//                if(result.get('actionCategory') == "Regulator"){
//                    //move to first
//                    uniqueResults.unshift(result);
//                    uniqueResults.splice(i+1, 1);
//                }
//            });
//
//            // BRING PETITION TO FRONT
//            $.each(uniqueResults,function(i,result){
//                if(result.get('actionCategory') == "Local Representative"){
//                    //move to first
//                    uniqueResults.unshift(result);
//                    uniqueResults.splice(i+1, 1);
//                }
//            });
//            console.log(uniqueResults)
//
//
//            //ADD DIVS FOR ACTIONS
//            for (var i = 0; i < uniqueResults.length; i++) {
//              var $listItem = $("<li>" + uniqueResults[i].get('actionCategory') + "</li>");
//              $listItem.attr("id", uniqueResults[i].get('actionCategory'));
//              $listItem.attr("class", "action-item");
//              $(".action-row").append($listItem);
//            }
//
//
//            // ADD DIVS FOR MENU
////            for (var i = 0; i < SortedResults.length; i++) {
////              $("#menu_list").append("<div><li>" + JSON.stringify(SortedResults[i], null, 4) + "</li></div>").addClass
////              ("list-unstyled");
////            }
//          },
//          error: function(error) {
//            alert("Error: " + error.code + " " + error.message);
//          }
//      });

//function getSegmentData(segmentId,programId){
//    console.log("segmentID")
//    console.log(segmentId);
//    console.log(programId);
//    // Query Parse for Segment and Program Info & update html (not menu items yet)
//    var Segment = Parse.Object.extend("Segments");
//    var query = new Parse.Query(Segment);
//    query.equalTo("_id", segmentId); //"JPGM9mmcKV"
//    query.find({
//        success: function(results) {
//            //change html
//            //$("#segment-title").text("/ " + results[0].get('segmentTitle'));
//            //$('#purpose-summary-text').text(results[0].get('purposeSummary') + " Share your thoughts below. ");
//
//            // Query program info
//            var Program = Parse.Object.extend("Programs");
//            var queryProgram = new Parse.Query(Program);
//            queryProgram.equalTo("_id", programId); //"JvW9oAYlo8"
//            queryProgram.find({
//                success: function(programResults) {
//                  //$("#segment-title").text("/ " + programResults[0].get('programTitle') + " / " + results[0].get
//                  //('segmentTitle'));
//                },
//                error: function(error) {
//                  alert("Error: " + error.code + " " + error.message);
//                }
//            })
//            },
//        error: function(error) {
//          alert("Error: " + error.code + " " + error.message);
//        }
//    });
//};