$(document).ready(function() {
  $("#browse-btn").on( "click", function() {
    window.location.href="http://127.0.0.1:8000/browse.com";
  });

  function addCategory(event) {
    console.log(event);
    categoryValue = $("#category").val();
    console.log(categoryValue);
    //$('#category').append("input");
    //$('#savedItems').append(categoryValue);
  };
});
//    $(".selector").on("change", function(event) {
//        console.log(event);
//        addCategory(event);
//    });

//    window.setInterval(function(){
//      var programType = $('#program-type').text()
//      if(programType == "documentary"){
//        $('#program-type').text("video")
//      } else {
//        $('#program-type').text("documentary")
//      }
//    }, 5000);




//query.equalTo("playerName", "Dan Stemkoski");
//      alert("here");






// <input t1qqype="file" id="profilePhotoFileUpload">

//

//    });

// TO OPEN A NEW WINDOW.
//var redirectWindow = window.open('', '_blank');
//      redirectWindow.location;
