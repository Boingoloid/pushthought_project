


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
            console.log("yes, data to return")
            console.log(data)
            var htmlText = [];
            htmlText = '<div style="margin-left:60px; font-size:11pt; color:gray;">required fields</div>';
            data.forEach(function (dict, i) {
                field = dict['value'];
                var bioguideId = dict['bioguideId'];
                var congressLastName = $('#'+bioguideId).text();
                //console.log(dict['value']);
                    //if(field == 'NAME_FIRST'){
                    var fieldName = field.replace('_','-');
                    //console.log('yes, first name');
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
                            console.log(optionsList.length);
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
               console.log(typeof(classText));
               console.log(classText);
               console.log(classText['input'].split(" "));
               var classWithBioguide = classText['input'].split(" ")[1];
               console.log(classWithBioguide);
               var bioguideId = classWithBioguide.replace('email-name-','');
               var found = false;
               $('.email-form-field-container').each(function(){
                    if($(this).hasClass(bioguideId)){
                        found  = true;
                        console.log("marking one of them as true");
                    }
               });
                if (found){
                    $('.email-name-'+bioguideId).text('click to toggle');
                } else {
                    $('.email-name-'+bioguideId).text('not integrated site link');
                }
            });

            // hide those not selected
            // hide all, show those with correct bioguide.  IF multi- loop show all for each bioguide



            $('.email-form-field-container').hide();
            var showArray = []
            $('.address-item-label:visible').each(function(){
                var bioguideId = $(this).attr('id');
                showArray.push(bioguideId);
            });
            console.log(showArray);
            for (var i = 0; i < showArray.length; i++) {
                $('.'+ showArray[i]).show();
            }













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
    $('.eform').each(function(){
        var fieldNode = $(this)
        var field = $(this).val();
        var fieldName = fieldNode.attr('id').replace('eform-','');
        console.log(fieldNode);
        console.log(field);
        console.log(fieldName);

        if (fieldNode.is('input')){
            if(field.length == 0){
                alert('all fields are required.  Please enter this field: ' + fieldName);
                validationResult = false;
                return false;
            }
        } else if (fieldNode.is('select')){
            var selection =  $(this).find(":selected").text();
            if(selection == 'select a topic'){
                console.log(fieldNode);
                alert("please enter a " + fieldName);
                validationResult = false;
                return false;
            } else {
            }
        }
    });

    // Validation email of if others have values
    if (validationResult){
        function validateEmail(email) {
            var re = /\S+@\S+\.\S+/;
            return re.test(email);
        }
        var email = $('.eform#eform-EMAIL').val();
        console.log(email);
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
    $('.eform').each(function(i){
        var field = String($(this).attr('id'));
        field = '$' + field.replace('eform-','').replace('-','_');
        formDataDictionary[field] = $(this).val();
    });
    var stringJson = JSON.stringify({
        "bio_id": bioguideId,
        "fields": formDataDictionary
    });
    console.log(stringJson);


    /*var dataSet = JSON.stringify({
            "tweet_text": tweet_text,
            "segment_id": segment_id,
            "program_id": program_id,
            "last_menu_url": window_url,
            "address_array" : addressArray,
    });
    console.log(dataSet);*/
    console.log("returning false because reached point before submittal")
    return false;

    $.ajax({url: "/submit_congress_email/",
        type: "POST",
        data: stringJson,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            console.log(data);
            if(data['status'] == 'success'){
                console.log("success status from ajax submit_congress_email");
                //show success
                $('.email-action-container').html('');
                var headerAllowance = $('.seen-it-container').offset().top - 20;
                $('html, body').animate({
                    scrollTop: headerAllowance + 'px'
                }, 'fast');
                showEmailSuccess(bioguideArray);

            } else if (data['status'] == 'captcha_needed'){
                console.log("need captcha received in ajax submit_congress_email");
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
                var errorMessageHTML = ['<div class="email-error"><p style="color:red;">'+ data['message'] +'</p></div>'].join("\n");
                $('.email-action-container').append(errorMessageHTML);
                    setTimeout(function(){ $('.email-error').remove(); }, 2000); // how long message shows
                    // info sits without changing, since likely resubmit.
            }
        },
        error: function() {
        }
    });
}

