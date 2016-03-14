

function addCategory(event) {
  console.log(event);
  categoryValue = $("#category").val();
  console.log(categoryValue);
  //$('#category').append("input");
  //$('#savedItems').append(categoryValue);
};

//    $(".selector").on("change", function(event) {
//        console.log(event);
//        addCategory(event);
//    });



$(document).ready(function() {

//    window.setInterval(function(){
//      var programType = $('#program-type').text()
//      if(programType == "documentary"){
//        $('#program-type').text("video")
//      } else {
//        $('#program-type').text("documentary")
//      }
//    }, 5000);


    var window_url =  window.location.href;

    Parse.initialize("lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM", "tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP");
    Parse.serverURL = 'https://ptparse.herokuapp.com/parse';

    // DECLARING VARIABLES FOR FETCHED DATA
    var menuData;
    var menuDataFiltered = [];

    $('.action-container').on('click','.action-item',function(event) {
        var selectedCategory = $(this).attr('id');
        console.log(selectedCategory);

        var menuDataFiltered = _.filter(menuData, function(item){
           return item.get('actionCategory') == selectedCategory;
        });

        if(selectedCategory == "Local Representative"){
            window.location.href="http://127.0.0.1:8000/action_menu/JvW9oAYlo8/JPGM9mmcKV/fed_representative.com";
        } else if(selectedCategory == "Petition") {
            window.location.href="http://127.0.0.1:8000/action_menu/JvW9oAYlo8/JPGM9mmcKV/fed_representative.com";
        } else {
            window.location.href="www.google.com";
        }
    });

      var SegmentIdentifier = $("#segmentId").text()

      // GET SEGMENT TITLE
      var Segment = Parse.Object.extend("Segments");
      var query = new Parse.Query(Segment);
      query.equalTo("_id", "JPGM9mmcKV"); //"JPGM9mmcKV"
      query.find({
        success: function(results) {
            $("#segment-title").text("/ " + results[0].get('segmentTitle'));
            $('#purpose-summary-text').text(results[0].get('purposeSummary') + " Share your thoughts below. ");
            var Program = Parse.Object.extend("Programs");
            var queryProgram = new Parse.Query(Program);
            queryProgram.equalTo("_id", "JvW9oAYlo8"); //"JvW9oAYlo8"
            queryProgram.find({
                success: function(programResults) {
                  $("#segment-title").text("/ " + programResults[0].get('programTitle') + " / " + results[0].get
                  ('segmentTitle'));
                },
                error: function(error) {
                  alert("Error: " + error.code + " " + error.message);
                }
            })
            },
        error: function(error) {
          alert("Error: " + error.code + " " + error.message);
        }
       });


        // GET MENU LIST DATA
      var MessageList = Parse.Object.extend("Messages");
      var query = new Parse.Query(MessageList);
      query.equalTo("segmentId", "JPGM9mmcKV");
      query.find({
          success: function(results) {

            // SORTING THE MESSAGE RESULTS
            var SortedResults = results.sort(function(a, b){
              var nA = a.get('actionCategory');
              var nB = b.get('actionCategory');
              if(nA < nB)
                return -1;
              else if(nA > nB)
                return 1;
              return 0;
            });

            // ASSIGN SORTED RESULTS TO VARIABLE - ACCESSED ON SELECTION OF CATEGORY
            menuData = SortedResults;

            // GET UNIQUE VALUES FOR ACTION MENU
            var uniqueResults = _.unique(SortedResults, false, function(item){
              return item.get('actionCategory');
            });

            // BRING LOCAL REP TO FRONT
            $.each(uniqueResults,function(i,result){
                if(result.get('actionCategory') == "Petition"){
                    //move to first
                    uniqueResults.unshift(result);
                    uniqueResults.splice(i+1, 1);
                }
            });

            // BRING REGULATOR TO FRONT
            $.each(uniqueResults,function(i,result){
                if(result.get('actionCategory') == "Regulator"){
                    //move to first
                    uniqueResults.unshift(result);
                    uniqueResults.splice(i+1, 1);
                }
            });

            // BRING PETITION TO FRONT
            $.each(uniqueResults,function(i,result){
                if(result.get('actionCategory') == "Local Representative"){
                    //move to first
                    uniqueResults.unshift(result);
                    uniqueResults.splice(i+1, 1);
                }
            });


            //ADD DIVS FOR ACTIONS
            for (var i = 0; i < uniqueResults.length; i++) {
              var $listItem = $("<li>" + uniqueResults[i].get('actionCategory') + "</li>");
              $listItem.attr("id", uniqueResults[i].get('actionCategory'));
              $listItem.attr("class", "action-item");
              $(".action-row").append($listItem);
            }


            // ADD DIVS FOR MENU
//            for (var i = 0; i < SortedResults.length; i++) {
//              $("#menu_list").append("<div><li>" + JSON.stringify(SortedResults[i], null, 4) + "</li></div>").addClass
//              ("list-unstyled");
//            }
          },
          error: function(error) {
            alert("Error: " + error.code + " " + error.message);
          }
      });
});



//query.equalTo("playerName", "Dan Stemkoski");
//      alert("here");






// <input t1qqype="file" id="profilePhotoFileUpload">

//

//    });

// TO OPEN A NEW WINDOW.
//var redirectWindow = window.open('', '_blank');
//      redirectWindow.location;
