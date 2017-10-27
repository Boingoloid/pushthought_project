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
const NAMES_OF_FIELDS_THAT_CAN_BE_DUPLICATED = ['ADDRESS_COUNTY', 'TOPIC']

const FIELDS_DATA_FOR_MEMBERS_UNSUPPORTED_BY_PHANTOM_DC = [
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$MESSAGE"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$SUBJECT"
    }, 
    {
        "maxlength": null, 
        "options_hash": [
            "Mr.", 
            "Mrs.", 
            "Ms.", 
        ], 
        "value": "$NAME_PREFIX"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$NAME_FIRST"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$NAME_LAST"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$EMAIL"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$PHONE"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$ADDRESS_STREET"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$ADDRESS_CITY"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$ADDRESS_ZIP5"
    }, 
    {
        "maxlength": null, 
        "options_hash": null, 
        "value": "$ADDRESS_ZIP4"
    }, 
    {
        "maxlength": null, 
        "options_hash": [
            "AL", 
            "AK", 
            "AZ", 
            "AR", 
            "CA", 
            "CO", 
            "CT", 
            "DE", 
            "DC", 
            "FL", 
            "GA", 
            "HI", 
            "ID", 
            "IL", 
            "IN", 
            "IA", 
            "KS", 
            "KY", 
            "LA", 
            "ME", 
            "MD", 
            "MA", 
            "MI", 
            "MN", 
            "MS", 
            "MO", 
            "MT", 
            "NE", 
            "NV", 
            "NH", 
            "NJ", 
            "NM", 
            "NY", 
            "NC", 
            "ND", 
            "OH", 
            "OK", 
            "OR", 
            "PA", 
            "RI", 
            "SC", 
            "SD", 
            "TN", 
            "TX", 
            "UT", 
            "VT", 
            "VA", 
            "WA", 
            "WV", 
            "WI", 
            "WY"
        ], 
        "value": "$ADDRESS_STATE_POSTAL_ABBREV"
    }, 
    {
        "maxlength": null, 
        "options_hash": [
            "Abortion",
            "Academy Nominations",
            "Adoption",
            "Affordable Care Act",
            "Afghanistan",
            "Aging",
            "Agriculture",
            "Animals",
            "Antitrust",
            "Appalachian Regional Commission",
            "Appropriations",
            "Arctic National Wildlife Refuge",
            "Armed Forces",
            "Armed Services",
            "Arts",
            "Assistance with a Federal Agency",
            "Autographed Photo",
            "Aviation",
            "Banking",
            "Behavioral Health",
            "Border Issues",
            "Border Security Caucus",
            "Border Security",
            "Broadband",
            "Budget (Defense)",
            "Budget (Federal)",
            "Budget",
            "Business",
            "Campaign Finance",
            "Campaign",
            "Children",
            "Civil Liberties",
            "Civil Rights",
            "Civil Service",
            "Clean Energy",
            "Climate",
            "Coastal Restoration",
            "Commerce",
            "Communications",
            "Congratulations Letter Request",
            "Congratulations",
            "Congress",
            "Congressional Issues",
            "Congressional Procedures",
            "Constituent Services",
            "Constitution",
            "Constitutional Amendment",
            "Consumer Affairs",
            "Consumer Protection",
            "Consumer Safety",
            "Corruption",
            "County Payments",
            "Courts",
            "Crime",
            "Culture",
            "Cybersecurity",
            "Death Penalty",
            "Debt Ceiling",
            "Defense",
            "Deficit Reduction",
            "Disability",
            "Disaster Relief",
            "Domestic Violence",
            "Drugs",
            "Eagle Scouts",
            "Economic Development",
            "Economics",
            "Education Higher",
            "Education K through 12",
            "Education",
            "Election Reform",
            "Elections",
            "Emergency Management",
            "Employment",
            "Endangered Species",
            "Energy",
            "Entitlements",
            "Environment (Clean Air, Clean Water, Waste)",
            "Environment Conservation",
            "Environment",
            "Ethics",
            "Export-Import Bank",
            "FDA",
            "FEMA",
            "Family Planning",
            "Family Values",
            "Family",
            "Federal Agency Assistance",
            "Federal Budget",
            "Federal Debt",
            "Federal Emergency Management",
            "Federal Employees Issues",
            "Federal Employees",
            "Federal Government Agencies",
            "Federal Spending",
            "Federal Survelliance",
            "Filibuster",
            "Finance",
            "Financial Crisis",
            "Financial Reform",
            "Financial Sector",
            "Financial Services",
            "First Amendment Rights",
            "Fish",
            "Fisheries",
            "Flags",
            "Flood Insurance",
            "Food Safety",
            "Food Stamps",
            "Food",
            "Foreclosures",
            "Foreign Affairs",
            "Foreign Aid",
            "Foreign Policy",
            "Foreign Relations",
            "Foreign Trade",
            "Forestry",
            "Gaming",
            "Gas Prices",
            "Global Warming",
            "Government Operations",
            "Government Politics",
            "Government Reform",
            "Government Shutdown",
            "Government Spending",
            "Government",
            "Grants",
            "Guns",
            "Hate Crimes",
            "Health Insurance",
            "Healthcare",
            "Historical Preservation",
            "History",
            "Homeland Security",
            "Housing",
            "Human Rights",
            "Human Trafficking",
            "Humanities",
            "Hunger",
            "Hurricane Preparedness",
            "Illegal Drugs",
            "Immigration",
            "Inauguration",
            "Indian Affairs",
            "Indian Country",
            "Infrastructure",
            "Insurance",
            "Intellectual Property",
            "Intelligence Issues",
            "Intelligence",
            "Interior",
            "Internal Revenue Service (IRS)",
            "International Affairs",
            "International Finance",
            "Internet",
            "Internship",
            "Iran",
            "Iraq",
            "Israel",
            "Job Creation",
            "Job Training",
            "Jobs",
            "Judicial Nominations",
            "Judiciary",
            "Justice",
            "LGBT issue",
            "LIHEAP",
            "Labor",
            "Law Enforcement",
            "Law",
            "Life",
            "Livestock",
            "Manufacturing",
            "Medicaid",
            "Medicare",
            "Meeting Request",
            "Mental Health",
            "Middle East",
            "Military Operations",
            "Military",
            "Mining",
            "Minority Issues",
            "Miscellaneous",
            "Monetary Policy",
            "Montana Values",
            "Municipal Government",
            "NASA",
            "National Labs",
            "National Parks",
            "National Security",
            "Native Americans",
            "Native Hawaiians",
            "Natural Disasters",
            "Natural Resources",
            "Newsletter",
            "Nominations",
            "North Africa",
            "Nuclear Proliferation",
            "Nuclear Weapons",
            "Nutrition",
            "Oil Prices",
            "Online Privacy",
            "Other",
            "Parks",
            "Passports",
            "Patents",
            "Peanuts",
            "Pension (Federal)",
            "Pension (Military)",
            "Pension",
            "Phone Call",
            "Postal Service",
            "Poultry",
            "Prescription Drugs",
            "President",
            "Press Request",
            "Privacy",
            "Public Assistance Programs",
            "Public Finance",
            "Public Lands",
            "Public Welfare",
            "Public Works",
            "Radio",
            "Recreation",
            "Regulatory Reform",
            "Religion",
            "Renewables",
            "Reproductive Health",
            "Reproductive Rights",
            "Retirement",
            "Rivers",
            "SNAP",
            "Scheduling Request",
            "Science",
            "Seafood",
            "Second Amendment Rights",
            "Securities",
            "Senate Procedure",
            "Seniors",
            "Service Academies",
            "Small Business",
            "Social Issues",
            "Social Sciences",
            "Social Security",
            "Social Welfare",
            "Solar",
            "Space",
            "Sports",
            "State Appropriations",
            "State Issues",
            "Surveillance",
            "TSA",
            "TV",
            "Taxes",
            "Technology",
            "Telecommunications",
            "Terrorism",
            "Terrorism",
            "Timber",
            "Tobacco",
            "Tort Reform",
            "Tourism",
            "Tours",
            "Trade",
            "Traditional Values",
            "Transportation",
            "U.S. Military Academies",
            "Unemployment",
            "Unions",
            "Urban Affairs",
            "Values",
            "Veterans",
            "Violence",
            "Visas",
            "WIC",
            "War in Iraq",
            "War on Terror",
            "Water Resources Development",
            "Water",
            "Waterfront",
            "Welfare",
            "Wild Horses",
            "Wildlife Protection",
            "Women",
            "Workforce",
            "Yucca Mountain"
        ], 
        "value": "$TOPIC"
    }
]


function preload_phantom_dc_members_data() {
    $.getJSON(
        '/static/js/phantom-dc-members.min.json',
        function(data) {
            $('.bioguide-mule').each(function () {
                var fields = [];
                if (this.id in data) {
                    fields_data = data[this.id]['required_actions'];
                } else {
                    fields_data =
                        FIELDS_DATA_FOR_MEMBERS_UNSUPPORTED_BY_PHANTOM_DC;
                }
                for (item of fields_data) {
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
            precreate_congress_email_fields();
        });
}


function get_form_data_list() {
    var form_data_list = [];
    $('.action-panel-container .bioguide-mule').each(function() {
        form_data_list.push($(this).data('form'));
    });
    return form_data_list
}


function show_hide_congress_email_fields() {
    var visible_fields_names = [];
    $('.action-panel-container.selected .bioguide-mule').each(function() {
        var form_data = $(this).data('form');
        if (form_data == undefined) {
            console.log("`show_hide_congress_email_fields` called before form" +
                        " data is loaded, exiting.");
            return;
        }
        for (var field of form_data) {
            var field_name = field['field_name'];
            if (NAMES_OF_FIELDS_THAT_CAN_BE_DUPLICATED.includes(field_name)) {
                field_name += '-' + field['bioguideId'];
            }
            field_name += '-container';
            visible_fields_names.push(field_name);
        }
    });
    $('.email-form-field-container').each(function () {
        $(this).toggle(visible_fields_names.includes(this.id));
    });
}


function precreate_congress_email_fields() {
    form_data_list = deduplicate_and_order_congress_email_fields(
        get_form_data_list());
    var htmlText = "";
    form_data_list.forEach(function (email_field, i) {
        var field_name = email_field['field_name'];
        // Select box with options.
        if (['TOPIC', 'ADDRESS_COUNTY', 'ADDRESS_STATE_POSTAL_ABBREV',
             'NAME_PREFIX'].includes(field_name)) {
            if (field_name == "ADDRESS_STATE_POSTAL_ABBREV") {
                var label_name = "ADDRESS_STATE";
            } else {
                var label_name = field_name;
            }
            var bioguide = email_field['bioguideId'];
            var bioguide_name = $('.email-name-' + bioguide).text();
            var last_name = bioguide_name.substring(
                bioguide_name.lastIndexOf(" ") + 1, bioguide_name.length);
            var class_bioguide = '';
            if (NAMES_OF_FIELDS_THAT_CAN_BE_DUPLICATED.includes(field_name)) {
                label_name += ' - ' + last_name;
                field_name += '-' + bioguide;
                class_bioguide = ' ' + bioguide;
            }
            var topic_class_name = field_name.toLowerCase() + '-container ' +
                field_name.toLowerCase() + '-container-' + bioguide;

            htmlText = [htmlText,
                '<div class="email-form-field-container ' + topic_class_name +
                '" style="display:block;" id="' + field_name + '-container">',
                '   <div class="label-div">',
                '<label for="eform-' + field_name +
                '" style="display:inline;" class="email-form-label' +
                class_bioguide + '">' + label_name + '</label>',
                '<select class="eform" id="eform-' + field_name + '"' +
                ' style="display:block;">',
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
                        '<option value="' + email_field['options'][key] + '">' + key + '</option>'
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
            /////////////////////////////////////////////////////
            // if field is ADDRESS_ZIP5
            // change name of label to ADDRESS_ZIP
            /////////////////////////////////////////////////////
            var label_name = field_name
            var readonly = '';
            if (field_name === 'ADDRESS_ZIP5') {
                label_name = 'ADDRESS_ZIP'
            }
            ///// not sure what this line is doing
            var value = emailFieldData[field_name] || '';
            /////////////////////////////////
            // If ADDRESS_ZIP% and value '' then grab zip from
            // zip-input elemennt on page.
            /////////////////////////////////
            if (field_name === 'ADDRESS_ZIP5') {
                readonly = 'readonly';
            }

            htmlText = [htmlText,
                '<div class="email-form-field-container" id="' + field_name +
                '-container" style="display:block;">',
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
    show_hide_congress_email_fields();
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
    for (member of form_data_list) {
        try {
            for (field of member) {
                if (!collected_field_names.includes(field['field_name']) ||
                        NAMES_OF_FIELDS_THAT_CAN_BE_DUPLICATED.includes(
                            field['field_name'])) {
                    data.push(field);
                    collected_field_names.push(field['field_name']);
                }
            }
        } catch (e) {
            // Probably won't reproduce anymore.
            alert("Error loading data, please refresh the page.")
            break;
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
            if (email_field['field_name'] == ordered_email_field) {
                email_field_to_add_to_array = email_field;
                ordered_email_fields.push(email_field_to_add_to_array);
            }
        });
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

    return $.ajax({url: "/submit_congress_email/",
        type: "POST",
        data: stringJson,
        contentType: 'json;charset=UTF-8',
        cache: false,
        success: function(data) {
            console.log("response from email send to phantom: ", data);
            if (data['status'] == 'success'){
                alert("Your e-mails have been sent.");
                //console.log("success status from ajax submit_congress_email:" + data);

                // Clear the email action container
                precreate_congress_email_fields();
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
            alert(
                "There was a problem sending your e-mails, please try again.");
        }
    });

}
