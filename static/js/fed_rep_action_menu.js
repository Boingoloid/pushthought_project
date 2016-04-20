

function createTitle(){
}

$(document).ready(function(){

    window.setTimeout(function() {
        $(".alert").fadeTo(3000, 0)
    }, 3000);

    var window_url =  window.location.href;

    Parse.initialize("lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM", "tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP");
    Parse.serverURL = 'https://ptparse.herokuapp.com/parse';

    var segmentId = $('#segmentId').text();
    //    "JPGM9mmcKV";
    var programId = $('#programId').text();
    //alert (segmentId);


    getCongressData();
    getHashtags(segmentId);
    getTweets(segmentId);

//    function getCongressData (){
//        var root = "https://congress.api.sunlightfoundation.com/legislators/locate";
//        var apiKey = "ed7f6bb54edc4577943dcc588664c89f";
//        var zipCode = "94107";
//
//        $.getJSON(root + "?zip=" + zipCode + "&apikey=" + apiKey,
//            function(data){
//                //console.log(data);
//                var bioguideArray = [];
//                var repHTML = '';
//                //$('.rep-container').append(repHTML);
//
//                $.each(data.results,function(i,rep){
//                  // CREATE BIOGUIDE ARRAY
//                  var bioguideID = rep.bioguide_id;
//                  bioguideArray.push(bioguideID);
//
//                  // CREATE NAME & TITLE
//                  var fullName = rep.first_name + " " + rep.last_name;
//                  var title = "";
//                  var chamber = rep.chamber;
//                  if(rep.chamber == "senate"){
//                   title = "Senator, " + rep.state;
//                  } else {
//                    title = "Rep, " + rep.state + " - d:" + rep.district;
//                  }
//                  defaultRepImage = ""
//
//                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
//                  repHTML += "<div class='rep-item' id='rep-item" + i + "'>";
//                  repHTML += "<p hidden id='tweet-address-item" + i + "'>@" + rep.twitter_id + "</p>";
//                  repHTML += "<img class='repPhoto'  id='repPhoto" + i + "' src=\"/static/img/seal-congress.png\"";
//                  repHTML +=  "alt='Portrait' width='60px' height='60px'>";
//                  repHTML += "<p>" + fullName + "</p>";
//                  repHTML += "<p>" + title + "</p>"
//                  repHTML += "</div>";
//                });
//                $('.rep-container').append(repHTML);
//                getCongressImages(bioguideArray);
//            }
//        ); // end getJSON
//
//        function getCongressImages(bioguideArray){
//
//            if(bioguideArray === undefined || bioguideArray.length == 0){
//                console.log('Congress array empty so not getting photos')
//
//            } else {
//                var CongressImages = Parse.Object.extend("CongressImages");
//                var query = new Parse.Query(CongressImages);
//                query.containedIn("bioguideID",bioguideArray);
//                query.find({
//                    success: function(results) {
//
//                      //INSERT PHOTOS
//                      $.each(results,function(i,repPhoto){
//                        var bioguideID = repPhoto.attributes.bioguideID
//                        //console.log(bioguideID);
//                        $.each(bioguideArray, function (i,repItem){
//                            var bid = repItem;
//                            if(bioguideID == bid){
//                            //console.log("yes");
//                                //get photo
//                                var imageFileURL = repPhoto.attributes.imageFile._url;
//                                $('#repPhoto' + i).attr("src",imageFileURL);
//                            } else {
//                            //console.log("no");
//                            }
//                        });
//                      });
//                    },
//                    error: function(error) {
//                      alert("Error: " + error.code + " " + error.message);
//                    }
//                })
//            }
//        }
//    }


//    function getHashtags(segmentId){
//          var hashtagList = Parse.Object.extend("Hashtags");
//          var query = new Parse.Query(hashtagList);
//          query.equalTo("segmentObjectId", "JPGM9mmcKV"); //"JPGM9mmcKV"
//          query.descending("frequency");
//          query.limit(1000);
//          //"email","Email","Long Form Email","phoneCall"
//          query.find({
//             success: function(results) {
//
//                var hashtagListHTML = '';
//                $.each(results,function(i,hashtag){
//
//                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
//                  hashtagListHTML += "<div class='hashtag-item'>";
//                  hashtagListHTML += "<p>" + hashtag.get('hashtag') + " | "
//                  hashtagListHTML += hashtag.get('frequency') + "</p>"
//                  hashtagListHTML += "</div>";
//                });
//                $('.hashtag-container').append(hashtagListHTML);
//             },
//            error: function(error) {
//              alert("Error: " + error.code + " " + error.message);
//            }
//          });
//    }


//    function getTweets(segmentId) {
//      var tweetList = Parse.Object.extend("sentMessages");
//      var query = new Parse.Query(tweetList);
//      query.equalTo("segmentId", "JPGM9mmcKV"); //"JPGM9mmcKV"
//      query.limit(1000);
//      query.contains("messageType","twitter");
//      //"email","Email","Long Form Email","phoneCall"
//      query.find({
//        success: function(results) {
//                var tweetListHTML = '';
//                $.each(results,function(i,tweet){
//                  // CREATE tweet flex item
//                  // CREATE HTML TO INSERT FOR FED REP FLEXBOX
//                  tweetListHTML += "<div class='tweet-item'>";
//                  tweetListHTML += "<p>" + tweet.get('messageText') + "</p>";
//                  tweetListHTML += "</div>";
//                });
//                $('.tweet-container').append(tweetListHTML);
//
//              var uniqueResults = _.unique(results, false, function(item){
//              return item.get('messageType');
//              });
//            },
//        error: function(error) {
//          alert("Error: " + error.code + " " + error.message);
//        }
//      });
//
//    }

    // CLICK ACTIONS
    $('.rep-container').on('click','.rep-item',function(event) {
       var idText = $(this).attr('id');
       var repIndex = idText.replace('rep-item','');
       var tweetAddressID = "#tweet-address-item" + repIndex;
       var tweetAddress = $(tweetAddressID).text();
       var currentText = $('#text-input').val();
       if($(this).css('background-color') === 'rgb(255, 255, 255)'){
         $(this).css('background-color','green');
         currentText += tweetAddress;
         $('#text-input').val(currentText);
       } else {
        $(this).css('background-color','white');
        var n = currentText.search(tweetAddress);
        //console.log(n);
        var re = new RegExp(tweetAddress,"gi");
        var newText = currentText.replace(re,"");
        $('#text-input').val(newText)
       }
    });

    $('.hashtag-container').on('click','.hashtag-item',function(event) {
       var idText = $(this).attr('id');
       var hashtagWithCount = $(this).text();
       var index = hashtagWithCount.search(" ");
       var hashtagText = hashtagWithCount.substr(0, index);
       var hashtagFrequency = hashtagWithCount.substr(index + 3, hashtagWithCount.length);
       var currentText = $('#text-input').val();
       //$(this).css('background-color','green');
       currentText += " " + hashtagText;
       $('#text-input').val(currentText);

    });

    $('.tweet-container').on('click','.tweet-item',function(event) {
      var tweetText = $(this).text()
      $('#text-input').val(tweetText);
    });

    $('#clear-button').on('click',function(event) {
        $('#text-input').val("");
    });

    $('#tweet-button').on('click',function(event) {

      var tweetText = $('#text-input').val();
      alert (tweetText);

      if(tweetText.length < 1){
        alert ("Please type a message to tweet first");
      } else {

        //Create and encode URL
        var encodedTweetText = encodeURIComponent(tweetText);
        // window_url = "http://www.pushthought.com/action_menu"
        window_url = "http://127.0.0.1:8000";
        window_url += "/verify_twitter/" + programId + "/" + segmentId;
        window_url += "/" + encodedTweetText;

        alert(window_url)
        window.location.href = window_url;

//        var csrftoken = Cookies.get('csrftoken');
//        alert("CSRF token:" + csrftoken);
//
//        function csrfSafeMethod(method) {
//        // these HTTP methods do not require CSRF protection
//            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
//        }
//        $.ajaxSetup({
//            beforeSend: function(xhr, settings) {
//                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
//                }
//            }
//        });
//
//        $.post("http://www.pushthought.com/action_menu/verify_twitter/",
//          {
//            tweetText: tweetText,
//            actionCategory: "Local Representative",
//            messageCategory: "Local Representative",
//            segmentId: segmentId,
//            programId: programId
//          }
//            );



      }

    });
});
