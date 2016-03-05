

function createTitle(){
}

$(document).ready(function(){
Parse.initialize("lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM", "tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP");
Parse.serverURL = 'https://ptparse.herokuapp.com/parse';

var segmentId = "JPGM9mmcKV";
getCongressData();
getHashtags(segmentId);
getTweets(segmentId);

    // CLICK ACTIONS
    $('.rep-container').on('click','.rep-item',function(event) {
        alert("rep clicked");

    });

    $('.hashtag-container').on('click','.hashtag-item',function(event) {
        alert("hashtag clicked");

    });

    $('.tweet-container').on('click','.tweet-item',function(event) {
        alert("tweet clicked");
    });
    
    function getCongressData (){
        var root = "https://congress.api.sunlightfoundation.com/legislators/locate";
        var apiKey = "ed7f6bb54edc4577943dcc588664c89f";
        var zipCode = "94107";

        $.getJSON(root + "?zip=" + zipCode + "&apikey=" + apiKey,
            function(data){
                var bioguideArray = [];
                var repHTML = '';
                //$('.rep-container').append(repHTML);

                $.each(data.results,function(i,rep){
                  // CREATE BIOGUIDE ARRAY
                  var bioguideID = rep.bioguide_id;
                  bioguideArray.push(bioguideID);

                  // CREATE NAME & TITLE
                  var fullName = rep.first_name + " " + rep.last_name;
                  var title = "";
                  var chamber = rep.chamber;
                  if(rep.chamber == "senate"){
                   title = "Senator, " + rep.state;

                  } else {
                    title = "Rep, " + rep.state + " - d:" + rep.district;
                  }
                  defaultRepImage = ""

                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
                  repHTML += "<div class='rep-item'>";
                  repHTML += "<img class='repPhoto'  id='repPhoto" + i + "' src=\"/static/img/seal-congress.png\"";
                  repHTML +=  "alt='Portrait' width='60px' height='60px'>";
                  repHTML += "<p>" + fullName + "</p>";
                  repHTML += "<p>" + title + "</p>"
                  repHTML += "</div>";
                });
                $('.rep-container').append(repHTML);
                getCongressImages(bioguideArray);
            }
        ); // end getJSON

        function getCongressImages(bioguideArray){

            if(bioguideArray === undefined || bioguideArray.length == 0){
                console.log('Congress array empty so not getting photos')

            } else {
                var CongressImages = Parse.Object.extend("CongressImages");
                var query = new Parse.Query(CongressImages);
                query.containedIn("bioguideID",bioguideArray);
                query.find({

                    success: function(results) {
                      //INSERT PHOTOS, ORDER MUST BE THE SAME AS BIOGUIDE IDS SUBMITTED
                      $.each(results,function(i,rep){
                        var imageFileURL = rep.attributes.imageFile._url;
                        $('#repPhoto' + i).attr("src",imageFileURL);
                      });
                    },

                    error: function(error) {
                      alert("Error: " + error.code + " " + error.message);
                    }
                })
            }
        }
    }


    function getHashtags(segmentId){


          var hashtagList = Parse.Object.extend("Hashtags");
          var query = new Parse.Query(hashtagList);
          query.equalTo("segmentObjectId", "JPGM9mmcKV"); //"JPGM9mmcKV"
          query.descending("frequency");
          query.limit(1000);
          //"email","Email","Long Form Email","phoneCall"
          query.find({
             success: function(results) {

                var hashtagListHTML = '';
                $.each(results,function(i,hashtag){

                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
                  hashtagListHTML += "<div class='hashtag-item'>";
                  hashtagListHTML += "<p>" + hashtag.get('hashtag') + " | "
                  hashtagListHTML += hashtag.get('frequency') + "</p>"
                  hashtagListHTML += "</div>";
                });
                $('.hashtag-container').append(hashtagListHTML);
             },
            error: function(error) {
              alert("Error: " + error.code + " " + error.message);
            }
          });
    }



    function getTweets(segmentId) {
      var tweetList = Parse.Object.extend("sentMessages");
      var query = new Parse.Query(tweetList);
      query.equalTo("segmentId", "JPGM9mmcKV"); //"JPGM9mmcKV"
      query.limit(1000);
      query.contains("messageType","twitter");
      //"email","Email","Long Form Email","phoneCall"
      query.find({
        success: function(results) {

                var tweetListHTML = '';

                $.each(results,function(i,tweet){
                  // CREATE tweet flex item

                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
                  tweetListHTML += "<div class='tweet-item'>";
                  tweetListHTML += "<p>" + tweet.get('messageText') + "</p>";
                  tweetListHTML += "<p>" + tweet.get('username') + "</p>"
                  tweetListHTML += "</div>";
                });
                $('.tweet-container').append(tweetListHTML);

              var uniqueResults = _.unique(results, false, function(item){
              return item.get('messageType');
            });


//            var Program = Parse.Object.extend("Programs");
//            var queryProgram = new Parse.Query(Program);
//            queryProgram.equalTo("_id", "JvW9oAYlo8"); //"JvW9oAYlo8"
//            queryProgram.find({
//                success: function(programResults) {
//                  $("#segment-title").text("/ " + programResults[0].get('programTitle') + " / " + results[0].get
//                  ('segmentTitle'));
//                },
//                error: function(error) {
//                  alert("Error: " + error.code + " " + error.message);
//                }
//            })
            },
        error: function(error) {
          alert("Error: " + error.code + " " + error.message);
        }
       });



    }
    //use parse to get tweets for segment, need segid
    $("#segmentId").text()

});
