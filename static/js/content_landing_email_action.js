//
//$('.test-button').click( function() {
//    console.log("no required fields data to return");
//    if(confirm("We don't have a webform for that congress person.  We will redirect you to your email client to reach them by their opencongress.org email address.")) {
//
//        var bioguideArray = 'F000464';
//        var mailto = $('#' + bioguideArray).attr('name');
//        var title = encodeURIComponent($('.title-header').text());
//        var description = encodeURIComponent($('.description').text());
//        var suggestedEmailText = encodeURIComponent($('.field-suggested-email').text());
//
//        //console.log('name: ' + mailto);
//        //console.log('title: ' + title);
//        //console.log('descr: ' + description);
//        console.log('suggestedEmailText: ' + suggestedEmailText);
//
//
//        if(!suggestedEmailText == ""){
//            location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + suggestedEmailText);
//            console.log('true');
//        } else {
//            location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + description);
//            console.log('false');
//        }
//
//    } else {
//        //do nothing
//    }
//});




function get_congress_email_fields(bioguideArray) {
    bioguideArrayString = JSON.stringify(bioguideArray);
    console.log('bioguide array string: ', bioguideArrayString);

    $.ajax({
        url: '/get_congress_email_fields/',
        type: "POST",
        data: bioguideArrayString,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function (data) {
            console.log("data from phantom: " ,data);
            ////////////////////////////////////////
            // returned data is congress email fields
            ///////////////////////////////////////

            if (!data) {
                console.log("no required fields data to return");

                if(confirm("We don't have a webform for that congress person.  We will redirect you to your email client to reach them by their opencongress.org email address.")) {

                    var bioguideArray = String(bioguideArray);
                    var mailto = $('#' + bioguideArray).attr('name');
                    var title = encodeURIComponent($('.title-header').text());
                    var description = encodeURIComponent($('.description').text());
                    var suggestedEmailText = encodeURIComponent($('.field-suggested-email').val());


                    //console.log('name: ' + mailto);
                    //console.log('title: ' + title);
                    //console.log('descr: ' + description);
                    //console.log('suggestedEmailText: ' + suggestedEmailText);

                    if(!suggestedEmailText == ""){
                        location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + suggestedEmailText);
                        //console.log('true');
                    } else {
                        location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + description);
                        //console.log('false');
                    }
                } else {
                    //do nothing
                }
                return false;
            }
            console.log("yes, required fields data to return");
            // console.log(data);
            var htmlText = [];


            ////////////////////////////////////////
            // order returned fields
            // function below
            ///////////////////////////////////////
            data = order_congress_email_fields(data);
            // console.log(data);


            /////////////////////////////////////////////////////////
            // adjust field names for display because some are long or odd
            // creates and inserts html for email form and inserts fields in HTMLobject .email-action-container
            /////////////////////////////////////////////////////////



            data.forEach(function (email_field, i) {
                var field_name = email_field['field_name'];
                //console.log("printing field name", field_name);
                //console.log('print options', email_field['options']);

                // If "TOPIC" make select box with options

                if((field_name == "TOPIC") || (field_name == "ADDRESS_STATE_POSTAL_ABBREV") || field_name == "NAME_PREFIX") {

                    if(field_name == "ADDRESS_STATE_POSTAL_ABBREV"){
                        var label_name = "ADDRESS_STATE";
                    } else {
                        var label_name = field_name;
                    }

                    htmlText = [htmlText,
                        '<div class="email-form-field-container" style="display:block;">',
                        '   <div class="label-div">',
                            '<label for="eform-' + field_name + '" style="display:inline;" class="email-form-label">' + label_name + '</label>',
                        // '</div>',
                        // '<div>',
                            '<select class="eform" id="eform-' + field_name + '" style="display:block;">',
                            '<option value=0 disabled="disabled" selected="selected">select</option>'
                        // '</div>',
                    ].join("\n");

                    // define optionList
                    var optionsList = email_field['options'];

                    /////////////////////////////////////////////////////////////
                    // detect if options list is dictionary or array, first array
                    /////////////////////////////////////////////////////////////
                    if(optionsList[0]){
                        //console.log('true - array');
                        for (var i = 0; i < optionsList.length; i++) {
                            htmlText = [htmlText,
                                '<option value="' + optionsList[i] + '">' + optionsList[i] + '</option>'
                            ].join("\n");
                        }

                    ////////////////////////////////////////////////////
                    // and now if dictionary
                    ////////////////////////////////////////////////////
                    } else {
                        //console.log('false - dict');
                        for (var key in optionsList){
                            htmlText = [htmlText,
                                '<option value="' + key + '">' + key + '</option>'
                            ].join("\n");
                        }
                    }
                    ////////////////////////////////////////////////////
                    // close options select box and field
                    ////////////////////////////////////////////////////
                    htmlText = [htmlText,
                        '</select>',
                        '</div>',
                        '</div>'
                    ].join("\n" );
                } else {
                    var label_name = field_name
                    var readonly = '';
                    if (field_name === 'ADDRESS_ZIP5') {
                        label_name = 'ADDRESS_ZIP'
                    }
                    var value = emailFieldData[field_name] || '';
                    if (field_name === 'ADDRESS_ZIP5') {
                        readonly = 'readonly'

                        if (!value) {
                            value = $('.zip-input').attr('value')
                        }

                    }

                    htmlText = [htmlText,
                        '<div class="email-form-field-container" style="display:block;">',
                            '<div class="label-div">',
                        ' <label for="eform-' + field_name + '" style="display:inline;" class="email-form-label">' +
                                    label_name + '</label>',
                            '</div>',
                            '<div class="field-div">',
                            '<input type="text" class="eform" id="eform-' + field_name + '" value="'+
                                    value +'" '+ readonly +'>',
                            '</div>',
                        '</div>'
                    ].join("\n");
                }
            });
            $('.email-action-container').append(htmlText);
            $('#text-input').val(emailFieldData['MESSAGE']);
        }
    });
}


/////////////////////////////////////////////////////////////
// function
// shows designated order of known fields
// orders them according to list
/////////////////////////////////////////////////////////////
function order_congress_email_fields(data) {
    var ordered_fields_key = [

        "SUBJECT",
        "NAME_PREFIX",
        "NAME_FIRST",
        "NAME_LAST",
        "EMAIL",
        "PHONE",
        "ADDRESS_STREET",
        "ADDRESS_CITY",
        "ADDRESS_ZIP4",
        "ADDRESS_ZIP5",
        "ADDRESS_STATE_POSTAL_ABBREV",
        "TOPIC"
    ];


    ///////////////////////////////////////////////////
    //put fields in order according to master list
    ///////////////////////////////////////////////////
    var ordered_email_fields = [];
    var email_field_to_add_to_array = {};
    var previous_field = "";
    ordered_fields_key.forEach(function (ordered_email_field) {
        data.forEach(function (email_field) {
            var field_name = email_field['field_name'];
            if(field_name == previous_field){
            } else {
                // if field name = field in list, then
                if (field_name == ordered_email_field) {
                    //console.log(field_name + " " + ordered_email_field);
                    email_field_to_add_to_array = email_field;
                    ordered_email_fields.push(email_field_to_add_to_array);

                } else {
                }
            }
            previous_field = field_name
        });
        // console.log("printing email field object", email_field_to_add_to_array);
        // console.log("printing field name", email_field_to_add_to_array);
    });

    ////////////////////////////////////////////////////////
    //put extra fields not in master ordered list at the end
    ////////////////////////////////////////////////////////

    var extra_fields_array = [];
    var match = false;
    data.forEach(function (email_field_object) {
        match = false;
        ordered_fields_key.forEach(function (ordered_email_field) {
            var field_name = email_field_object['field_name'];
            if (field_name == ordered_email_field) {
                match = true;
                // do nothing, field already in list
            }
        });
        email_field_to_add_to_array = email_field_object;
        if (match) {

        } else {
            //console.log("extra field:" + email_field_object['field_name'])
            extra_fields_array.push(email_field_to_add_to_array);
        }
    });
    return ordered_email_fields.concat(extra_fields_array);

}






    /*
    var match = false;
    var ordered_email_fields = [];
    var extra_fields_array = [];
    var email_field_to_add_to_array = {};

    data.forEach(function (email_field_object) {
        match = false;
        ordered_fields_key.forEach(function (ordered_email_field) {
            var field_name = email_field_object['field_name'];
            if(field_name == ordered_email_field){
                match = true;
            }
        });
        email_field_to_add_to_array = email_field_object;
        if(match){
            ordered_email_fields.push(email_field_to_add_to_array);
            console.log("push:" + email_field_object['field_name']);
        } else {
            console.log("extra field:" + email_field_object['field_name'])
            extra_fields_array.push(email_field_to_add_to_array);
        }
    });

    // console.log(ordered_email_fields);
    return ordered_email_fields.concat(extra_fields_array);
    */


            /*
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
                            });
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
            var showArray = [];
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
                })
                }
            });



        },
        error: function() {
            console.log('failure in get email fields content_landing.js');
        }
    });
}*/


//////////////////////////////////////////////////////////
// send email to api
//
//////////////////////////////////////////////////////////


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
        var fieldNode = $(this);
        var field = $(this).val();
        var fieldName = fieldNode.attr('id').replace('eform-','');

        //////////////////////////////////////////////////////
        // Validate all inputs have values
        //////////////////////////////////////////////////////

        if (fieldNode.is('input')){
            if(field.length == 0){
                alert('all fields are required.  Please enter this field: ' + fieldName);
                validationResult = false;
                return false;
            }

        //////////////////////////////////////////////////////
        // Validate 'select a topic' is selected
        //////////////////////////////////////////////////////

        } else if (fieldNode.is('select')){
            var selection =  $(this).find(":selected").text();
            if(selection == 'select'){
                alert("please enter a " + fieldName);
                validationResult = false;
                return false;
            } else {
            }
        }
    });

    //////////////////////////////////////////////////////
    // Validate email field
    //////////////////////////////////////////////////////
    if (validationResult){
        function validateEmail(email) {
            var re = /\S+@\S+\.\S+/;
            return re.test(email);
        }
        var email = $('.eform#eform-EMAIL').val();
        if (validateEmail(email)){
            console.log("email is good.");
        } else {
            //console.log("email is bad");
            alert("Email enetered is not a valid email.  Please check and try again.");
            return false;
        }
    } else {
        return false;
    }
    ////////////////////////////////////////////////////////
    // Create dict for send
    ////////////////////////////////////////////////////////
    var formDataDictionary = {};
    $('.eform:visible').each(function(i){
        var field = String($(this).attr('id'));
        field = '$' + field.replace('eform-','').replace('-','_');
        //field = field.replace('eform-','').replace('-','_');
        //console.log(field);
        if(field == '$ADDRESS_ZIP'){
            field = '$ADDRESS_ZIP5';
        }
        //if(field == '$TOPIC'){
        //    formDataDictionary[field] = 'ARTS';
        //} else {
            formDataDictionary[field] = $(this).val();
        //}
    });
    var insertDict = {};
    //insertDict['$EMAIL'] = 'matthew.acalin@gmail.com'
    //formDataDictionary = $.extend({},formDataDictionary, insertDict);

    formDataDictionary['$MESSAGE'] = $('#text-input').text();
    //var programId = $('#programId').text();
    var stringJson = JSON.stringify({
        "bio_id": bioguideId,
        //"program_id": programId,
        "campaign_tag": "push_thought",
        "fields": formDataDictionary
    });
    console.log("showing json string prior to send email to phantom API: ", stringJson);


    //put agax call here to store values in session.

    $.ajax({url: "/submit_congress_email/",
        type: "POST",
        data: stringJson,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            console.log("response from email send to phantom: ", data);
            if(data['status'] == 'success'){
                alert("Your email has been sent ");
                //console.log("success status from ajax submit_congress_email:" + data);

                // Clear the email action container
                $('.email-action-container').html('');
                // Excute close button
                $('#close-button').trigger('click');

                ///////////////////////////////////////////////
                // Scroll the window up
                ///////////////////////////////////////////////
                //if($('.seen-it-container')){
                //    var headerAllowance = $('.seen-it-container').offset().top - 20;
                //    $('html, body').animate({
                //        scrollTop: headerAllowance + 'px'
                //    }, 'fast');
                //}

                //showEmailSuccess(bioguideArray);


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

