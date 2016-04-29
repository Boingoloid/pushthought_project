$(document).ready(function() {
    window.setTimeout(function() {
        $(".alert").fadeTo(3000, 0)
    }, 3000);

    //function validationFunc(){
        $('#create-form').validate({ // initialize the plugin
            rules: {
                user_email: {
                    required: true,
                    email: true
                },
                password: {
                    required: true,
                    minlength: 5
                },
                confirm_password: {
                    required: true,
                    minlength: 5,
                    equalTo: "#password"
                }
            },
            messages: {
                user_email: {
                    required: "Please enter a valid email"
                },
                password: {
                    required: "Please enter a password",
                    minlength: "must be at least 5 characters long"
                },
                confirm_password: {
                    required: "Please confirm password",
                    minlength: "must be at least 5 characters long",
                    equalTo: "Passwords must match"
                }
            },
            submitHandler: function(form) {
                csrftoken =
                function csrfSafeMethod(method) {
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                }

                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });

                $.post("http://127.0.0.1:8000/aaform_submittal/", $("#create-form").serialize());
                 console.log("Do some stuff...");
                 //submit via ajax
                  return false;  //This doesn't prevent the form from submitting.
            }
        });


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



//    $('#create-account-btn').click(function() {
//        email = $('#email').val();
//        password = $('#password').val();
//        confirm_password = $('#confirm_password').val();

//        if (email.length ==0 || password.length ==0 || confirm_password.length ==0){
//            alert("please fill out all the fields");
//        } else {
//            console.log("length");
//            console.log(email.length);

//            validationFunc();




});





//var password = document.getElementById("password")
//  , confirm_password = document.getElementById("confirm_password");
//
//function validatePassword() {
//  if (password.value != confirm_password.value) {
//    confirm_password.setCustomValidity("Passwords Don't Match");
//  } else {
//    confirm_password.setCustomValidity('');
//  }
//}
//
//password.onchange = validatePassword;
//confirm_password.onkeyup = validatePassword;