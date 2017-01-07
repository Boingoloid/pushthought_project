$(document).ready(function() {

    window.setTimeout(function() {
        $(".alert").fadeTo(2000, 0)
    }, 2000);

    $("#browse-btn").on("click",function(){
//        $('html, body').animate(window.scrollTo(0, 1350));
            window.scrollTo(0, 1350);
//            window.location.href="browse/";

    });


  $("#submit-email-btn").on("click",function(){
//    alert("I am an alert box!");
    //window.location.href="submit-email"

    var email = $("#email").val();

    if (email.length == 0 ){
        alert("Please enter an email. :)");
    } else if (!email.match(/@/)){
        alert("The @ symbol is needed for a valid email");
    } else {
        alertString = "Thank you, the email " + email + " has been submitted";
        alert(alertString);
        var redirectString = "submit-email/" + email;
        var encodedRedirectString = encodeURI(redirectString);
        window.location.href=encodedRedirectString;
    };
  });
});