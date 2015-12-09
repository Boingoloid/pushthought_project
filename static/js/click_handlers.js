function addCategory(event) {
  console.log(event);
  categoryValue = $("#category").val();
  console.log(categoryValue);
  //$('#category').append("input");
  //$('#savedItems').append(categoryValue);




};

$(document).ready(function() {
    $(".selector").on("change", function(event) {
        console.log(event);
        addCategory(event);
    });
});
