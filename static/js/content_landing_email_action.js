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


function preload_phantom_dc_members_data() {
    $.getJSON(
        '/static/js/phantom-dc-members.min.json',
        function(data) {
            $('.bioguide-mule').each(function () {
                var fields = [];
                for (item of data[this.id]['required_actions']) {
                    if (item['value'] != '$MESSAGE') {
                        var field_dict = [];
                        field_dict['field_name'] = item['value'].slice(1);
                        field_dict['bioguideId'] = this.id;
                        if (item['options_hash']) {
                            field_dict['options'] = item['options_hash'];
                        }
                        fields.push(field_dict);
                    }
                }
                $(this).data('form', fields);
            });
        }
    );
}


function get_congress_email_fields(form_data_list) {
    if (!form_data_list) {
        //console.log("no required fields data to return");

        //if(confirm("We don't have a webform for that congress person.  We will redirect you to your email client to reach them by their opencongress.org email address.")) {

        //    var bioguideArray = String(bioguideArray);
        //    var mailto = $('#' + bioguideArray).attr('name');
        //    var title = encodeURIComponent($('.title-header').text());
        //    var description = encodeURIComponent($('.description').text());
        //    var suggestedEmailText = encodeURIComponent($('.field-suggested-email').val());


        //    //console.log('name: ' + mailto);
        //    //console.log('title: ' + title);
        //    //console.log('descr: ' + description);
        //    //console.log('suggestedEmailText: ' + suggestedEmailText);

        //    if(!suggestedEmailText == ""){
        //        location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + suggestedEmailText);
        //        //console.log('true');
        //    } else {
        //        location.href = ("mailto:" + mailto + "?subject=" +title + "&body=" + description);
        //        //console.log('false');
        //    }
        //} else {
        //    //do nothing
        //}
        return false;
    }
    console.log("yes, required fields data to return");
    // get topic list for each topic value
    
    // put all email fields into one large list
//    fields_array = []
//    for (i in data){
//
//        console.log(data[i]);
//        object1 = data[i];
//        var bioguideId = Object.keys(object1)[0];
//        //console.log(String(bioguideId));
//        fields = data[i][bioguideId]['required_actions'];
//        //console.log(fields);
//        fields_array = fields_array.concat(fields);
//    }
//    console.log('fields array', fields_array);

    // Remove $ sign

    // alphabatize

//    for (j in fields_array){
//        console.log(fields_array[j]['value'].replace('$',''));
//        fields_array[j]['value'].replace('$','');

//        fields_array[j].replace('$','');
//    }


    // get 3 topic fields with bioguide id and options hash
//    var sorted = fields_array.sort(function(a, b) {
//        return a.value - b.value;
//    });

//    var fields_sorted = Object.keys(dict).map(function(key) {
//        return [key, dict[key]];
//    });
//    fields_array = fields_array.sort(function(a, b){return a-b});
//    console.log('fields array sorted', sorted);
    //eliminate duplicates
    //load with all fields plus topics

    var htmlText = [];

    ////////////////////////////////////////
    // order returned fields
    // function below
    ///////////////////////////////////////
    form_data_list = deduplicate_and_order_congress_email_fields(
        form_data_list);

    /////////////////////////////////////////////////////////
    // adjust field names for display because some are long or odd
    // creates and inserts html for email form and inserts fields in HTMLobject .email-action-container
    /////////////////////////////////////////////////////////

    form_data_list.forEach(function (email_field, i) {
        var field_name = email_field['field_name'];

        // Select box with options.
        if (field_name == "TOPIC" ||
                field_name == "ADDRESS_COUNTY" ||
                field_name == "ADDRESS_STATE_POSTAL_ABBREV" ||
                field_name == "NAME_PREFIX") {

            if (field_name == "ADDRESS_STATE_POSTAL_ABBREV") {
                var label_name = "ADDRESS_STATE";
            } else {
                var label_name = field_name;
            }
            var bioguide = email_field['bioguideId'];
            var bioguide_name = $('.email-name-' + bioguide).text();
            var last_name = bioguide_name.substring(
                bioguide_name.lastIndexOf(" ") + 1, bioguide_name.length);
            var label_name = label_name + ' - ' + last_name;
            var topic_class_name = field_name.toLowerCase() + '-container ' +
                field_name.toLowerCase() + '-container-' + bioguide;

            htmlText = [htmlText,
                '<div class="email-form-field-container ' + topic_class_name +
                '" style="display:block;">',
                '   <div class="label-div">',
                '<label for="eform-' + field_name + '" style="display:inline;" class="email-form-label ' + bioguide + '">' + label_name + '</label>',
                '<select class="eform" id="eform-' + field_name + '" data-bioguide="' + bioguide + '" style="display:block;">',
                '<option value=0 disabled="disabled" selected="selected">select</option>'
            ].join("\n");

            if (Array.isArray(email_field['options'])) {
                for (var i = 0; i < email_field['options'].length; i++) {
                    htmlText = [htmlText,
                        '<option value="' + email_field['options'][i] + '">' +
                        email_field['options'][i] + '</option>'
                    ].join("\n");
                }
            } else {
                // Not an array, assume dictionary.
                for (var key in email_field['options']){
                    htmlText = [htmlText,
                        '<option value="' + key + '">' + key + '</option>'
                    ].join("\n");
                }
            }
            // Close options select box and field.
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
    $('.email-action-container').html(htmlText);
    $('#text-input').val(emailFieldData['MESSAGE']);

    $('.topic-container').hide();
    $('.action-panel-container').each(function(){
        if($(this).hasClass('selected')){
            var bioId = $(this).children().children('.bioguide-mule').attr('id');
            console.log("bioId: ", bioId);
            console.log('topic-container-'+ bioId);
            $('.topic-container-'+ bioId).show();
        }
    });
}


/////////////////////////////////////////////////////////////
// function
// shows designated order of known fields
// orders them according to list
/////////////////////////////////////////////////////////////
function deduplicate_and_order_congress_email_fields(form_data_list) {
    var ordered_fields_key = [
        "SUBJECT",
        "NAME_PREFIX",
        "NAME_FIRST",
        "NAME_LAST",
        "EMAIL",
        "PHONE_PARENTHESES",
        "PHONE",
        "ADDRESS_STREET",
        "ADDRESS_STREET_2",
        "ADDRESS_CITY",
        "ADDRESS_COUNTY",
        "ADDRESS_ZIP5",
        "ADDRESS_ZIP4",
        "ADDRESS_ZIP_PLUS_4",
        "ADDRESS_STATE_POSTAL_ABBREV",
        "TOPIC",
        "CAPTCHA_SOLUTION",
    ];

    // Collect fields from all members.
    var data = [];
    var collected_field_names = [];
    var names_of_fields_that_can_be_duplicated = ['NAME_PREFIX',
        'ADDRESS_COUNTY', 'ADDRESS_STATE_POSTAL_ABBREV', 'TOPIC']
    for (member of form_data_list) {
        // FIXME Sometimes raises "TypeError: member is undefined" until page
        // reload.
        for (field of member) {
            if (collected_field_names.indexOf(field['field_name']) == -1 ||
                    names_of_fields_that_can_be_duplicated.indexOf(
                        field['field_name']) != -1) {
                data.push(field);
                collected_field_names.push(field['field_name']);
            }
        }
    }

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


function runEmail(bioguideIds){
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
        if ($(this).data('bioguide')) {
            field += '_' + $(this).data('bioguide')
        }
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
        "bio_ids": bioguideIds,
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
