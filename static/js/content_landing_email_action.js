


function get_congress_email_fields(bioguideId){
    baseURL = 'https://congressforms.eff.org';
    endpoint = '/retrieve-form-elements';

//    bioguide = '{"bio_ids": ["C000880", "A000360"]}

    $.ajax({url: '/get_congress_email_fields/',
        type: "POST",
        data: bioguideId,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {

            console.log(data)
            var htmlText = [];
            data.forEach(function (dict, i) {
                field = dict['value'];
                //console.log(dict['value']);
                    //if(field == 'NAME_FIRST'){
                    var fieldName = field.replace('_','-');
                    //console.log('yes, first name');
                    if(fieldName == 'TOPIC'){
                        htmlText = [htmlText,
                        '<div class="email-form-field-container" style="display:block;">',
                            '<div class="label-div">',
                                '<label for="eform-'+ fieldName +'" style="display:inline;" class="email-form-label">'+ fieldName +':</label>',
                            '</div>',
                            '<div class="field-div">',
                                '<select class="eform" id="eform-'+ fieldName +'" style="display:block;">',
                                '<option value=0 disabled="disabled" selected="selected">select a topic</option>'
                        ].join("\n");
                        var optionsList = dict['options_hash'];
                        console.log(optionsList);

                        for (option in optionsList){
                            htmlText = [htmlText,
                                    '<option value="' +option +'">'+option+'</option>',
                            ].join("\n");
                        }
                        htmlText = [htmlText,
                                '</select>',
                            '</div>',
                        '</div>'
                        ].join("\n");
                    } else if(fieldName == 'MESSAGE'){
                        htmlText = htmlText;
                    } else {
                        htmlText = [htmlText,
                        '<div class="email-form-field-container" style="display:block;">',
                            '<div class="label-div">',
                                '<label for="eform-'+ fieldName +'" style="display:inline;" class="email-form-label">'+ fieldName +':</label>',
                            '</div>',
                            '<div class="field-div">',
                                '<input type="text" class="eform" id="eform-'+ fieldName+'">',
                            '</div>',
                        '</div>'].join("\n");
                    }
            });
            htmlText = [htmlText,
            '<div class="captcha-container"></div>'].join("\n");
            $('.email-action-container').append(htmlText);
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

    // validate email
    function validateEmail(email) {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }

    /*var email = $('.eform#eform-EMAIL').val();
    console.log(email);
    if (validateEmail(email)){
        //console.log("email is good.");
    } else {
        //console.log("email is bad");
    }


    // validate no blank fields
    $('.eform').each(function(){
    //console.log($(this));
        var field = $(this).val();
        if (field){
            if(field.length == 0){
                alert('all fields are required:' + field);
                return false;
            }
        } else {
            alert('please select a topic');
            return false;
        }
    });*/

    console.log('you made it');
    // create json

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

    $.ajax({url: "/submit_congress_email/",
        type: "POST",
        data: stringJson,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            console.log(data);
            if(data['status'] == 'success'){
                //show success
                $('.email-action-container').html('');
                var headerAllowance = $('.seen-it-container').offset().top - 20;
                $('html, body').animate({
                    scrollTop: headerAllowance + 'px'
                }, 'fast');
                showEmailSuccess(bioguideArray);

            } else if (data['status'] == 'captcha_needed'){
                // show captcha
                var captchahtml = ['<div><p>Copy the text</p></div>',
                '<div><p>from the image</p></div>',
                '<div><img class="captcha-img" src="'+data['url']+'"></div>',
                '<div><input type="text" class="captcha-input"></div>',
                '<div><button id="captcha-button">submit</button></div>'
                '<div class="captcha-alert"></div>',
                '<div hidden id="emailData" data-emailData="'+stringJson+'"></div>'
                ].join("\n");

//                HERE'S' HOW
//                var data = $('#alertList').data('alertlist');

                $('captcha-container').append(captchahtml);
            } else if (data['status'] == 'error'){
                console.log('error message:' + data['message']);
                var errorMessageHTML = ['<div class="email-error"><p style="color:red;">'+ data['message'] +'</p></div>'].join("\n");
                $('.email-action-container').append(errorMessageHTML);
                    setTimeout(function(){ $('.email-error').remove(); }, 2000); // how long message shows
                    // info just sits without changing.
            }
        },
        error: function() {
        }
    });
}