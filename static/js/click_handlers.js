

function addCategory(event) {
  console.log(event);
  categoryValue = $("#category").val();
  console.log(categoryValue);
  //$('#category').append("input");
  //$('#savedItems').append(categoryValue);
};





$(document).ready(function() {
    Parse.initialize("lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM", "tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP");
    Parse.serverURL = 'https://ptparse.herokuapp.com/parse';

    $(".selector").on("change", function(event) {
        console.log(event);
        addCategory(event);
    });

    $("#loadPhotos").click(function(event) {
    alert("loadPhotos");
    });


      var SegmentIdentifier = $("#segmentId").text()
      console.log(String(SegmentIdentifier));

      // GET SEGMENT TITLE
      var Segment = Parse.Object.extend("Segments");
      var query = new Parse.Query(Segment);
      query.equalTo("_id", "JPGM9mmcKV"); //"JPGM9mmcKV"
      query.find({
        success: function(results) {
            $("#segment-title").text("/ " + results[0].get('segmentTitle'));
            $('#textarea').text(results[0].get('purposeSummary') + " Share your thoughts below. ");
            var Program = Parse.Object.extend("Programs");
            var queryProgram = new Parse.Query(Program);
            queryProgram.equalTo("_id", "JvW9oAYlo8"); //"JvW9oAYlo8"
            queryProgram.find({
                success: function(programResults) {
                  console.log(programResults);
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


        // GET MESSAGE DATA
      var MessageList = Parse.Object.extend("Messages");
      var query = new Parse.Query(MessageList);
      query.equalTo("segmentID", "VICE1");
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



            // GET UNIQUE VALUES FOR ACTION MENU
            var uniqueResults = _.unique(SortedResults, false, function(item){
              return item.get('actionCategory');
            });
            console.log(uniqueResults);

            //ADD DIVS FOR ACTIONS
            for (var i = 0; i < uniqueResults.length; i++) {
              var $listItem = $("<li>" + uniqueResults[i].get('messageCategory') + "</li>");
              $listItem.attr("id", "X" + i);
              $listItem.attr("class", "action-item");
              $(".action-container").append($listItem);
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
