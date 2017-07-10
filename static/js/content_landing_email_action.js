


function get_congress_email_fields(bioguideArray){
    console.log("get congress email field firing.:" + bioguideArray);
    bioguideArrayString = JSON.stringify(bioguideArray);

    //bioguide = '{"bio_ids": ["C000880", "A000360"]}

    $.ajax({url: '/get_congress_email_fields/',
        type: "POST",
        data: bioguideArrayString,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            if(!data){
                console.log("no data to return")
                return false;
            }
            console.log("yes, data to return: get congress email fields")
            console.log(data)
            var htmlText = [];
            // htmlText = '<div id="required-fields-label" style="margin-left:60px; font-size:11pt; color:gray;">required fields</div>';
            data.forEach(function (dict, i) {
                field = dict['value'];
                var bioguideId = dict['bioguideId'];
                var congressLastName = $('#'+bioguideId).text();
                    var fieldName = field.replace('_','-');
                    if(fieldName == 'TOPIC'){
                    // set up the select
                        htmlText = [htmlText,
                        '<div class="email-form-field-container '+ bioguideId +'" style="display:block;">',
                            '<div class="label-div">',
                                '<label for="eform-'+ fieldName +'" style="display:inline;" class="email-form-label">'+ fieldName +' - '+ congressLastName +':</label>',
                            '</div>',
                            '<div class="field-div">',
                                '<select class="eform" id="eform-'+ fieldName +'" style="display:block;">',
                                '<option value=0 disabled="disabled" selected="selected">select a topic</option>'
                        ].join("\n");

                        // define optionList
                        var optionsList = dict['options_hash'];

                        // if array or dictionary, list the options
                        if(Array.isArray(optionsList)){
                            //console.log(optionsList.length);
                            for (var i = 0; i < optionsList.length; i++) {
                                htmlText = [htmlText,
                                        '<option value="' + optionsList[i] +'">'+optionsList[i]+'</option>'
                                ].join("\n");
                            }
                        } else {

                            // alphabetize keys for display
                            keys = Object.keys(optionsList);
                            keys.sort(function(a, b){
                                if(a < b) return -1;
                                if(a > b) return 1;
                                return 0;
                            })
                            for (var i = 0; i < keys.length; i++) {
                                htmlText = [htmlText,
                                        '<option value="' + keys[i] +'">'+keys[i]+'</option>'
                                ].join("\n");
                            }
                        }

                        // Close the select HTML object
                        htmlText = [htmlText,
                                '</select>',
                            '</div>',
                        '</div>'
                        ].join("\n");
                    } else if(fieldName == 'MESSAGE'){
                        htmlText = htmlText;
                    } else {
                        htmlText = [htmlText,
                        '<div class="email-form-field-container '+ bioguideId +'" style="display:block;">',
                            '<div class="label-div">',
                                '<label for="eform-'+ fieldName +'" style="display:inline;" class="email-form-label">'+ fieldName +':</label>',
                            '</div>',
                            '<div class="field-div">',
                                '<input type="text" class="eform" id="eform-'+ fieldName+'">',
                            '</div>',
                        '</div>'].join("\n");
                    }
            });
            // add captcha container
            htmlText = [htmlText,
            '<div class="captcha-container"></div>'].join("\n");

            // append the HTML
            $('.email-action-container').append(htmlText);


            // label which emails are available on email-name
            $('.email-name').each(function(){
               var classText = $(this).attr("class").match(/email-name-/);
               var classWithBioguide = classText['input'].split(" ")[1];
               var bioguideId = classWithBioguide.replace('email-name-','');
               var found = false;
               $('.email-form-field-container').each(function(){
                    if($(this).hasClass(bioguideId)){
                        found  = true;
                    }
               });
                if (found){
                    $('.email-name-'+bioguideId).text('form below');
                } else {
                    $('.email-name-'+bioguideId).text('not integrated');
                }
            });

            // hide all, show those with correct bioguide.  IF multi- loop show all for each bioguide
            $('.email-form-field-container').hide();
            var showArray = []
            $('.address-item-label:visible').each(function(){
                var bioguideId = $(this).attr('id');
                showArray.push(bioguideId);
            });
            for (var i = 0; i < showArray.length; i++) {
                $('.'+ showArray[i]).show();
            }



            // Fill in user data into form fields
            console.log("just before each");




            $('.eform').each(function(){
                var fieldName = $(this).attr("id");
                fieldName = fieldName.replace('eform-','');
                console.log(fieldName);
                var data = $('#emailFields').data('emailfields');
                if(data){
                    console.log("hello data:"+ data);
                    var fields = data['fields'];
                    console.log("fields:"+ fields);
                    Object.keys(fields).forEach(key => {
                            let value = fields[key];
                            keyNew = key.replace('_','-').replace('$','');
                            if(fieldName == keyNew){
                                console.log("key match" + fieldName);
                                $(this).val(value);
                            }
                    });
                }
            });



        },
        error: function() {
            console.log('failure in get email fields content_landing.js');
        }
    });
}

function runEmail(bioguideId){

    // validate text input not blank
    var message_text = $('#text-input').text();
    if(message_text.length < 1){
        alert ("Please type a message first");
        return false;
    }

    // validate no blank fields
    var validationResult = true;
    $('.eform:visible').each(function(){
        var fieldNode = $(this)
        var field = $(this).val();
        var fieldName = fieldNode.attr('id').replace('eform-','');

        if (fieldNode.is('input')){
            if(field.length == 0){
                alert('all fields are required.  Please enter this field: ' + fieldName);
                validationResult = false;
                return false;
            }
        } else if (fieldNode.is('select')){
            var selection =  $(this).find(":selected").text();
            if(selection == 'select a topic'){
                alert("please enter a " + fieldName);
                validationResult = false;
                return false;
            } else {
            }
        }
    });

    // Validate email if others pass validation first
    if (validationResult){
        function validateEmail(email) {
            var re = /\S+@\S+\.\S+/;
            return re.test(email);
        }
        var email = $('.eform#eform-EMAIL').val();
        if (validateEmail(email)){
            console.log("email is good.");
        } else {
            console.log("email is bad");
            alert("Email enetered is not a valid email.  Please check and try again.");
            return false;
        }
    } else {
        return false;
    }

    // Create dict for send
    var formDataDictionary = {};
    $('.eform:visible').each(function(i){
        var field = String($(this).attr('id'));
        field = '$' + field.replace('eform-','').replace('-','_');
        formDataDictionary[field] = $(this).val();
    });
    formDataDictionary['$MESSAGE'] = $('#text-input').text();
    var programId = $('#programId').text();
    var stringJson = JSON.stringify({
        "bio_id": bioguideId,
        "program_id": programId,
        "fields": formDataDictionary
    });
    console.log(stringJson);

    $.ajax({url: "/submit_congress_email/",
        type: "POST",
        data: stringJson,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            console.log(data);
            if(data['status'] == 'success'){
                console.log("success status from ajax submit_congress_email:" + data);

                // Clear the email action container
                $('.email-action-container').html('');
                // Excute close button
                $('#close-button').trigger('click');

                var headerAllowance = $('.seen-it-container').offset().top - 20;
                $('html, body').animate({
                    scrollTop: headerAllowance + 'px'
                }, 'fast');

                //showEmailSuccess(bioguideArray);
                alert("Your email has been sent ");

            } else if (data['status'] == 'captcha_needed'){
                console.log("need captcha received in ajax submit_congress_email:" + data);
                // show captcha
                var captchahtml = ['<div><p>Copy the text</p></div>',
                '<div><p>from the image</p></div>',
                '<div><img class="captcha-img" src="'+data['url']+'"></div>',
                '<div><input type="text" class="captcha-input"></div>',
                '<div><button id="captcha-button">submit</button></div>',
                '<div class="captcha-alert"></div>',
                '<div hidden id="emailData" data-emailData="'+stringJson+'"></div>',
                '<div hidden class="captcha-uid">'+ data['uid'] +'</div>'
                ].join("\n");


                //HERE'S' HOW
                //var data = $('#alertList').data('alertlist');
                //go to main content landing?  and make action for captcha submit button, include email data.


                $('captcha-container').append(captchahtml);
            } else if (data['status'] == 'error'){
                console.log('error message, email submit:' + data['message']);
                var errorMessageHTML = ['<div class="email-error"><p style="color:red;">'+ data['message'] +' Please try again.</p></div>'].join("\n");
                $('.email-action-container').append(errorMessageHTML);
                //setTimeout(function(){ $('.email-error').remove(); }, 5000); // how long message shows
                    // info sits without changing, since likely resubmit.
            }
        },
        error: function() {
        }
    });
}

