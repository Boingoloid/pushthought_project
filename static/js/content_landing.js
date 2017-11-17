//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");


function set_email_message_addressing_prefix() {
    selected_members = $('.address-item.selected');
    if (selected_members.length == 0) {
        html = '';
    } else if (selected_members.length == 1) {
        html = 'Congressperson ' + selected_members.children('p').text() + ', ';
    } else {
        html = 'Congressperson [name will be inserted], ';
    }
    $('#text-input .address-placeholder').html(html);
}


function focus_on_text_input() {
    text_input = $('#text-input')
    text_input.focus();
    setEndOfContenteditable(text_input);
}


$(document).ready(function() {

    var windowURL = window.location.href;

    // Facebook and Twitter sharing buttons
    var current_url = window.location.href;
    var fb_text = $("p.description").text().length ? $("p.description").text() : 'I just contacted my congressional reps on Push Thought'
    params = {
      'text': 'I just contacted my congressional reps on Push Thought',
      'url': current_url
    }
    $("#twitter-share-button").prop('href', "https://twitter.com/intent/tweet?"+$.param(params));

    $("#facebook-share-button").click(function(){
      FB.ui({
        method: 'share',
        href: current_url,
        quote: fb_text,
      }, function(response){});
    });

        // Zip submission button click
    $('.submit-zip').click(function() {
        function request_finished() {
            $('.submit-zip').prop('disabled', false);
        }

        if ($(this).prop('disabled')) {
            return false;
        }
        // validators
        var zip = $('.zip-input').val();
        var isValidZip = /(^\d{5}$)/.test(zip);

        if (isValidZip){
            $(this).prop('disabled', true);
            $('#zip-loader').show();
            console.log('valid zip');
            console.log('get_congres on zip:' + zip);
            $('.zip-input').attr('id',zip);
            $('.zip-input').attr('value',zip);
            deferred = get_congress(zip, get_congress_url);
            if (deferred) {
                deferred.done(request_finished);
                deferred.done(preload_phantom_dc_members_data);
                deferred.fail(request_finished);
            } else {
                request_finished();
            }
        } else{
            console.log('NOT a valid zip');
            alert('Not a valid zip code.  Please check and try again.')
            $('.zip-input').focus();
            $(this).show();
        }
    });

    var zip = $('.zip-input').val();
    if (zip) {
        $('.submit-zip').trigger('click');
    }

    // CSRF settings
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // on paste insert text
    $(document).on('paste','[contenteditable]',function(e) {
        e.preventDefault();
        var text = (e.originalEvent || e).clipboardData.getData('text/plain');
        window.document.execCommand('insertText', false, text);
    });


    // Success indicator (user already contacted) hover over
    $('.success-indicator').mouseenter(function() {
        var id = $(this).attr('id');
        idContainer = id.replace('success-indicator-','warning-box-indicator-');
        idText = id.replace('success-indicator-','indicator-text-');
        $('#'+ idContainer).show()
        $('#' + idText).show()
    });
    $('.success-indicator').mouseleave(function() {
        var id = $(this).attr('id');
        idContainer = id.replace('success-indicator-','warning-box-indicator-');
        idText = id.replace('success-indicator-','indicator-text-');
        $('#'+ idContainer).hide()
        $('#' + idText).hide()
    });


    // change cursor for action panel to pointer if action items visible
    $('.action-panel-container').mouseenter(function() {
        if($("#text-input:visible").length==1){
            $(this).css({"cursor": "pointer"});
        }
    });
    $('.action-panel-container').mouseleave(function() {
        $(this).css({"cursor": "default"});
    });

    $('.zip-indicator').click(function(){
        if ($('.zip-reset:visible')){
            $('.zip-reset').hide();
        } else{
            $('.zip-reset').show();
        }
    });


    // Zip indicator hover
    $('.zip-indicator').mouseenter(function() {
       $('.zip-reset').show();
    });

    $('.zip-reset-hover-boundary').mouseleave(function() {
        $('.zip-reset').hide();
    });


    // Location icon and zip reset
    $('.zip-reset').click(function() {
        // hide button
        $(this).hide();
        // clear the fed reps
        $('.rep-container').html('');
        // clear the address items
        $('.address-item').each(function(){
            $(this).remove();
        });
        // show zip capture
        $('.zip-capture').show();
        // hide zip indicator
        $('.zip-indicator').hide();
        // close action area if open
        $('#close-button').trigger('click');
        $('.zip-input').focus();
        $('.submit-zip').show();

        //Show title warning
        $('.category-title').hide();
        $('.category-warning').show();

    });


    $('.location-icon').click(function(){
        $('#zip-loader').show();
        //alert("Still in Development: Our location finder is being built, please enter you zip using the box below.  We'll move the cursor there for you :)");
        //$('.zip-input').focus();
        var lat;
        var long;
        //var x = document.getElementById("demo");
        function getLocation() {
            if (navigator.geolocation) {
                console.log("yes geo location");
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                alert("Geolocation is not supported by this browser or permission denied.");
            }
        }

        function showPosition(position) {
            lat = position.coords.latitude;
            long = position.coords.longitude;
            console.log("here");
            $.getScript('/static/js/content_landing_get_congress.js', function(){
                getCongressWithLocation(lat,long);
            });


        }
        getLocation();

    });




//    $('.zip-input').focusin(function(){
//        $('.submit-zip').show();
//    });


    // show/hide zip submit button if focus on zip-input
    $(document).mouseup(function(){
        if ($('.zip-input').is(":focus")){
            $('.submit-zip').show();
        } else {
            // $('.submit-zip').hide();
        }
    });


    // Prevent mutiple clicking of submit zip
    $('.zip-input').keydown(function(thisEvent){
      if (thisEvent.keyCode == 13) { // enter key
        thisEvent.preventDefault();

        if($('.zip-loader:visible').length > 0){
            return false;
        } else{
            $('.submit-zip').trigger('click');
        }
      }
    });




    // Watch button
    $('.watch-button').click( function() {
        alert("Watch function not in place yet, working on it. thanks :)");
    });

    // Select All Buttons

    $('.rep-container').on("click", "img.email-icon-all", function(e) {
        if ($('.twitter-name:visible').length) {
            return false;
        }
        if (!$('.email-name:visible').length) {
            $('.email-icon').first().click();
        }
        $('.action-panel-container').not('.selected').children(
            '.selection-panel').click();
    });

    $('.rep-container').on("click", "img.twitter-icon-all", function(e) {
        if ($('.email-name:visible').length) {
            return false;
        }
        if (!$('.twitter-name:visible').length) {
            $('.twitter-icon').first().click();
        }
        $('.action-panel-container').not('.selected').children(
            '.selection-panel').click();
    });

    $('.rep-container').on(
        "click", ".rep-item-container-all .status-panel", hide_status);

    // Email Icon
    $('.rep-container').on("click", "img.email-icon", function(e) {
        set_active_mode('selection');
        set_active_channel('email');
        //$('.copy-last').show();
        $('.copy-last').hide();
        e.stopPropagation();
        var emailIconId = $(this).attr('id');
        var i = emailIconId.replace('email-icon-','')
        //        console.log("i:" + i);
        // Previous version, just sends to webform
        //if ($(this).attr('id').length < 5 ){
        //    alert('sorry, no email form yet for this person.');
        //} else {
        //    var contactPath = $(this).attr('id');
        //    window.open(contactPath);
        //}
        //window.open('mailto:test@example.com?subject=subject&body=body');

        // stop if animation in progress
        // prevents button from getting hit twice
        if ($(':animated').length > 0) {
            return false;
        }

        // show action container and it's contents
        $('.rep-action-container').css('display','block'),400,function(){
        };
        $('.rep-action-container').animate({'opacity':'1.0'});
        $('.rep-action-container').animate({'display':'block'});
        $('.email-action-container').show();

        // scroll to appropriate place on screen to see action container
//        $('.category-container').animate({'height':'350px'},200,function(){
//            var headerAllowance = $('.seen-it-container').offset().top - 20;
//            $('html, body').animate({
//                scrollTop: headerAllowance + 'px'
//            }, 'fast');
//        });

        // expand containers
        $('#text-input').animate({'height':'200px','max-height':'200px'});



        // show email names
        $('.email-name').show();

        // Hide letter count
        $('.letter-count').hide();

        // select or toggle selection of activity container
        $('.action-panel-container#'+i).addClass("selected");

        // create address items above text input
        $('.email-name').each(function( index ){
           index = index + 1; //add 1 because this index starts at 0 as where HTML forloop it matches starts at 1
           var full_name = $(this).attr('name');
           var classText = $(this).attr("class").match(/email-name-/);
           var classWithBioguide = classText['input'].split(" ")[1];
           var bioguideId = classWithBioguide.replace('email-name-','');

           var text = ['<div class="address-item address-node-'+ index +'">',
                            '<p class="address-item-label address-item-label-'+index +'" id='+bioguideId+'>'+full_name+'</p>',
                      '</div>'].join('\n');
           $(".address-container").append(text);
        });

        // select address according to button clicked
        $(".address-node-" + i).toggleClass("selected");

        $('#text-input').html(
            '<span contenteditable=false class="address-placeholder"></span>')
        set_email_message_addressing_prefix();

        // text-input clear and increase height
        //$('#text-input').html('');
        //$('.address-placeholder').html('');
        //$('#text-input').css({"height":"100px","max-height":"100px"});

        // insert address placeholder in text-input
        //stringSpace = '&nbsp';
        //$('#text-input').html('<span contenteditable=false class=address-placeholder></span>');

        // show Send button and label , hide Tweet button and label
        $('#img-send-tweet-icon').hide();
        $('#tweet-button-label').hide();
        $('#img-send-email-icon').show();
        $('#email-button-label').show();

        // send label count
        countSelected = 0;
        $('.address-item').each(function(){
            if($(this).hasClass('selected')){
                countSelected = countSelected + 1;
            }
        });

        // Set email label
        var labelText = 'email: ' + countSelected;
        $('#email-button-label').text(labelText);


        updateTextCount();

//         Fill in fields with info from user
//        var data = $('#emailFields').data('emailfields');
//        if(data){
//            console.log("hello data:"+ data);
//            var fields = data['fields'];
//            console.log("fields:"+ fields);
//            for (item in fields){
//
//            }
//
//
//
//        } else {
//            console.log("no fields data");
//        }
        //<div hidden id="emailFields" data-emailFields="{{ currentUser.congressEmailFields }}"></div>
        show_hide_congress_email_fields();
        focus_on_text_input();
    });

    // Twitter Icon
    $('.rep-container').on("click", "img.twitter-icon", function(e) {
        set_active_mode('selection');
        set_active_channel('twitter');
        $('.copy-last').hide();
        e.stopPropagation();
        var i = $(this).attr('id');

        // if animation occuring, stop method
        // prevent from getting clicked multiple times
        if ($(':animated').length > 0) {
            console.log("returning false");
            return false;
        };

        // show action container
        $('.rep-action-container').show();
        $('.rep-action-container').animate({'opacity':'1.0'});
        $('.rep-action-container').animate({'display':'block'});
        $('#text-input').animate({'height':'200px','max-height':'200px'});

        // scroll to appropriate place on screen to see action container
//        $('.category-container').animate({'height':'350px'},200,function(){
//            var headerAllowance = $('.seen-it-container').offset().top - 20;
//            $('html, body').animate({
//                scrollTop: headerAllowance + 'px'
//            }, 'fast');
//        });

        // expand containers
//        $('.rep-color-band').animate({'height':'455px'});
//        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});

        // show Send button and label , hide Email button and label
        $('.img-send-tweet-icon').show();
        $('.tweet-button-label').show();
        $('.email-button-label').hide();
        $('.img-send-email-icon').hide();


        // select or toggle selection of activity container
        $('.action-panel-container#'+i).addClass("selected");

        // create address items above text input
        $('.twitter-name').each(function( index ){
           index = index + 1; //add 1 because this index starts at 0 as where HTML forloop it matches starts at 1
           var address = $(this).text();
           var bioguideId = $(this).attr('name');
           var text = ['<div class="address-item address-node-'+ index +'" name="'+ bioguideId +'">',
                            '<p class="address-item-label address-item-label-'+index +'">'+address+'</p>',
                      '</div>'].join("\n");
           $('.address-container').append(text);
        });
        // select address according to button clicked
        //console.log(".address-node-" + i);
        $(".address-node-" + i).toggleClass("selected");

        // insert address placeholder in text-input
        var addressPlaceholderClass = '.address-item-label-' + i;
        var addressPlaceholder = $(addressPlaceholderClass).text();
        addressPlaceholder = String(addressPlaceholder); // Space important! allows @ to be recognized
        $('#text-input').html('<span contenteditable=false class="address-placeholder">'+addressPlaceholder+' </span>');
        //<p class="space-placeholder" style="display:inline;"> </p>

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems;
        $('#tweet-button-label').text(labelText);

        updateTextCount();
        focus_on_text_input();
    });

    // Empty Twitter Icon
    $('.rep-container').on("click", "img.twitter-icon-empty", function(e) {
        e.stopPropagation();
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        }
        $('.warning-box-tweet-icon').css({'opacity':'1'});
        $('.warning-box-tweet-icon').animate({'opacity':'0.0'},2500,function() {});
    });

    // Phone icon
    $('.rep-container').on("click", "img.phone-icon", function(e) {
        e.stopPropagation();
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        var phone = $('.phone-icon').attr('id');
        var fullname = $(this).attr('name');
        var message = 'Making call to ' + fullname + '\'s DC office: ' + phone + '  Leave a message with your info and thoughts.';
        var makeCall = confirm(message);
        if (makeCall){
            window.location.href='tel:' + phone;
        } else {
            return false;
        }
    });


    // Empty Email Icon
    $('.rep-container').on("click", "img.email-icon-gray", function(e) {
        e.stopPropagation();
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        alert('sorry, no email form yet for this person.  Pleaes call or tweet.');
    });

    $('#close-button').on('click', function() {
        close_form();
        if ($('.rep-container').hasClass('active-mode-selection')) {
            set_active_mode('action');
        }
    });

    $('.rep-container').on('click', '.selection-panel', function() {
        container = $(this).parent();
        //////////////////////////////////////
        // get number of action panel clicked
        //////////////////////////////////////
        var index = container.attr('id');

        //////////////////////////////////////////////////////
        // get twitter name if twitter names visible
        //////////////////////////////////////////////////////
        if($('.twitter-name').is(":visible")){
            var elementRef = "#email-name-" + index;
            var elementText = $('#twitter-name-' + index).text();
            var whichIconClicked = "tweet";
            ////////////////////////////////////////////////////////////
            // if email visible
            ////////////////////////////////////////////////////////////
        } else if($('.email-name').is(":visible")){
            var whichIconClicked = "email";
        } else {
            return false;
        }

        // Adjust the highlight of selected/unselected container and add/remove
        // twitter handle above the input box.
        if (container.hasClass( "selected" )){
            container.removeClass('selected');
            var addressPath = ".address-node-" + index;
            $(addressPath).removeClass('selected');
        } else {
            container.addClass('selected');
            var addressPath = ".address-node-" + index;
            $(addressPath).addClass('selected');
        }

        // show and hide topic fields
        $('.topic-container').hide();
        $('.action-panel-container').each(function(){
            if(container.hasClass('selected')){
                var bioId = container.children().children(
                    '.bioguide-mule').attr('id');
                console.log("bioId: ", bioId);
                console.log('topic-container-'+ bioId);
                $('.topic-container-'+ bioId).show();
            }
         });

        ////////////////////////////////////////////////////////////
        // adjust the button and button label number
        ///////////////////////////////////////////////////////////
        var numItems = $('.address-item.selected').length;
        console.log("number of items: "+numItems);
        // Change button label
        if (whichIconClicked == "email"){
            var labelText = 'email: ' + numItems;
            $('#email-button-label').text(labelText);
        } else{
            var labelText = 'tweet: ' + numItems;
            $('#tweet-button-label').text(labelText);
        }
        ///////////////////////////////////////////////////////////
        // grabbing length of placeholder text and value of #textInput
        ///////////////////////////////////////////////////////////
        var placeholderLength = $('.address-placeholder').text().length
        var value = $('#text-input').html();
        console.log("placeholder length: " + placeholderLength);
        console.log("html value: " + value);

        ///////////////////////////////////////////////////
        // add placeholder if one does not exist
        //////////////////////////////////////////////////
        if (!$('.address-placeholder').length) {
            console.log("there is no placeholder");
            var value = $('#text-input').html();
            $('#text-input').html('<span contenteditable=false class=address-placeholder></span>' + value);
        }

        // Adjust placeholder text.
        if ($('.email-name').is(':visible')) {
            set_email_message_addressing_prefix();
            show_hide_congress_email_fields();
        } else {
            if (numItems == 0) {
                placeholderText = '';
                $('.address-placeholder').text(placeholderText);
            } else if (numItems == 1) {
                placeholderText = $(
                    '.address-item.selected').children('p').html();
                console.log('placeholder text for one:', placeholderText);
                placeholderText = placeholderText + ' ';
                $('.address-placeholder').text(placeholderText);
            } else {
                placeholderText = '@multiple';
                // endspace important so @ recognized
                placeholderText = placeholderText + ' ';
                $('.address-placeholder').text(placeholderText);
            }
        }
        focus_on_text_input();
    });

    // Clear button
    $('#clear-button').on('click',function(event) {
        var addressPlaceholder = $('.address-placeholder');
        $('#text-input').html(addressPlaceholder);

    });

    // Include Link checkbox
    $('#img-checked-box').on('click',function(event) {
        if ($(':animated').length) {
            return false;
        }
        //alert('The link is always included for context')
        $('.warning-box').css({'opacity':'1'});
        $('.warning-box').animate({'opacity':'0.0'},2500,function() {
        });
    });


    //////////////////////////////////////////////////
    /// problem with below method as it fires
    /// multiple timems when it should only fire once.
    ///////////////////////////////////////////////

    $("#text-tweet-block").on('DOMSubtreeModified', "#text-input", function() {
        updateTextCount();
        return false;
    });

    // Key Up: replaces placeholder if missing, updates count, updates selected
    $('#text-input').keyup(function() {

        /////////////////////////////////////////////////////
        // count letters and update letter count
        /////////////////////////////////////////////////////
        updateTextCount();

        //////////////////////////////////////////////////////////////////
        // Check if placeholder still exists
        //////////////////////////////////////////////////////////////////




        var value = $('#text-input').html();


          //$('#text-input').html('<span contenteditable=false class=address-placeholder></span>' + value);
            //    console.log("text-input-html 2: " + $('#text-input').html());


        //console.log("text-input-html 1: " + value);
        //console.log("placeholder text: " + $('.address-placeholder').text());
        //var placeholderLength = $('.address-placeholder').text().length;
        if (!$('.address-placeholder').length) {

            ////////////////////////////////////////////////////////
            // if twitter visible, then replace address placeholder
            /////////////////////////////////////////////////////////

            if($('.twitter-name').is(":visible")){
                //$('#text-input').html('<span contenteditable=false class=address-placeholder> </span>' + value);
                console.log("text-input-html 2: " + $('#text-input').html());

                //<p class="space-placeholder" style="display:inline;"> </p>
                $('.action-panel-container').removeClass('selected');
                $('.address-item').removeClass('selected');

                ////////////////////////////////////////////////////////
                // Change button label for every address-item selected
                /////////////////////////////////////////////////////////
                /*countSelected = 0;
                $('.address-item').each(function(){
                    if($(this).hasClass('selected')){
                        countSelected = countSelected + 1;
                    }
                });*/
             }


            ////////////////////////////////////////////////////////
            // Change button label for every selected
            // For email is 1
            // For tweet 0
            // Because address-placeholder just added back
            /////////////////////////////////////////////////////////
            //countSelected = 0;
            //if($('.email-name').is(":visible")){
            //    var email_name = $('.email-name:visible').attr('name');
            //     $('#text-input').html('<span contenteditable=false class=address-placeholder>Congessperson ' + email_name + ', </span>' + value);
            //     //<p class="space-placeholder" style="display:inline;"> </p>
            //     $('.email-name:visible').parent().parent().addClass('selected');
            //    countSelected = countSelected + 1;
            //    var labelText = 'email: ' + countSelected;
            //    $('#email-button-label').text(labelText);
            //} else {
            //    var labelText = 'tweet: ' + countSelected;
            //    $('#tweet-button-label').text(labelText);
            //}
        }


        //var textValue =  $('#text-input').html();
        //searchSpaceBool = value.search("<p class=\"space-holder\"");
        //if (searchSpaceBool == -1){
            //console.log("not there");
            //$( ".address-placeholder").after( "<p class=\"space-placeholder\" style=\"display:inline;\"></p>");
        //} else {
            //console.log("yes there");
            //$('#text-input').html('<p class="space-placeholder" style="display:inline;"> </p>' + textValue);
            //searchSpaceBool = value.search("<p class=\"space-container\"");
            //if (searchBool == -1){
        //}



    });

    // TWEET/EMAIL Button
    $('#tweet-button').click(function() {
        function request_finished() {
            hideLoading();
        }

        if ($(this).prop('disabled')) {
            return false;
        }
        if ($('.address-item.selected').length == 0) {
            alert("You much choose a congressperson.");
            return false;
        }
        $(this).prop('disabled', true);
        if ($('.email-name').is(":visible")){
            var bioguideIds = $('.address-item-label:visible').map(
                function() { return this.id }).get();
            deferred = runEmail(bioguideIds);
        } else {
            deferred = runTweet(windowURL);
        }
        if (deferred) {
            showLoadingForSelectedMembers();
            deferred.done(request_finished);
            deferred.fail(request_finished);
        } else {
            request_finished();
        }
    });

//    function updateEmailFieldsInSession(){
//        var fieldData = {}
//
//        $('.eform').each(function () {
//            var fieldName = $(this).attr('id');
//            fieldName = fieldName.replace('eform-','');
//            var fieldValue = $(this).val();
//            if(fieldName != 'TOPIC'){
//                fieldData[fieldName] = fieldValue;
//            }
//
//        });
//        console.log('field data: ',fieldData);
//        var fieldDataString = JSON.stringify({fieldData});
//        //store in session
//        $.ajax({url: "/store_email_fields_in_session/",
//            type: "POST",
//            data: fieldDataString,
//            contentType: 'json;charset=UTF-8',
//            cache: false,
//            success: function(data) {
//                console.log("email fields saved to session");
//            }
//        });
//    }


    $('.email-action-container').on("click", "#captcha-button", function(e) {
        // submit the capture via ajax and using the uid etc that are needed

        var captchaInput = $('captcha-input').val();
        var uid = $('.captcha-uid').text();
        var data = $('#emailData').data('emailData');
    //-d '{"answer": "cx9bp", "uid": "example_uid"}'


        var data = JSON.stringify({
            "answer": captchaInput,
            "uid": uid,
        });
        console.log(stringJson);

        $.ajax({url: "/submit_congress_captcha/",
            type: "POST",
            data: stringJson,
            contentType: 'json;charset=UTF-8',
            cache: false,
            success: function(data) {
                console.log(data);
                if(data['status'] == 'success'){
                    //show success
                } else if (data['status'] == 'error'){
                    // show error: captcha failed, please retry
                    $('.captcha-error').text(data['message']);
                    $('.captcha-error').show();
                    console.log('error message:' + data['message']);
                    setTimeout(function(){ $('.captcha-error').hide(); }, 2000);
                    }
            },
            error: function() {
            }
        });
    });

    function SelectText(element) {
        var doc = document;
        var text = element[0];
        var range;
        var selection;

        if (doc.body.createTextRange) {
            range = document.body.createTextRange();
            range.moveToElementText(text);
            range.select();
        } else if (window.getSelection) {
            selection = window.getSelection();
            range = document.createRange();
            range.selectNodeContents(text);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }

    $('.hashtag-container').on("click", ".hashtag-item", function(e) {
        // Copy hashtag text to Clipboard
        var element = $(this).children('.hashtag').contents();
        SelectText(element);
        document.execCommand("copy");

        // Show Copy to Clipboard indicator
        var element = $(this).children('.copied-to-clipboard')
        element.show();
        element.animate({"height":"47"},400,function(){
            setTimeout(function(){
                element.animate({"height":"0"},400,function(){
                    element.hide();
                });
             }, 400);
        });
    });

    $('.tweet-container').on("click", ".tweet-item", function(e) {
        // Copy tweet text to Clipboard
        var element = $(this).children('.tweet').contents();
        SelectText(element);
        document.execCommand("copy");

        // Show Copy to Clipboard indicator
        var element = $(this).children('.copied-to-clipboard')
        element.show();
        element.animate({"height":"47"},400,function(){
            setTimeout(function(){
                element.animate({"height":"0"},400,function(){
                    element.hide();
                });
             }, 400);
        });
    });

    $('.tweet_suggested_message_container').on(
        "click", ".field-suggested-tweet", function(e) {
            e.stopPropagation();
            var message = $(this).val();
            if ($('.rep-action-container').is(":hidden")) {
                $('.twitter-icon').click();
            }
            pasteMessage(message);
    });

    $('.email_suggested_message_container').on("click", ".field-suggested-email", function(e) {
        e.stopPropagation();
        console.log($('.tweet-button-label').text().slice( 0, 5 ));

        var sliced_string = $('.tweet-button-label').slice( 0, 5 )
        sstring = String(sliced_string);

        if($('.rep-action-container').is(":visible") && $('.tweet-button-label').is(":visible")){
            alert("Sorry, you can't paste email text into a tweet.");
            return false;
        }


        var message = $(this).val();

        if($('.rep-action-container').is(":visible")){
            //var address_placeholder_text = $('.address-placeholder').text();
            //console.log(address_placeholder_text);
        }else{
            $('.email-icon').trigger('click');
            //$('.address-placeholder').after('\n'+message);
        }

        pasteMessage(message);
        ////////// append message in input after span node
        //$('.address-placeholder').remove();
    });

    function pasteMessage(message){
        ////////// grab placeholder text
        placeholder_text = $('.address-placeholder').text();

        ////////// reinsert black placeholder span
        $('#text-input').html("<span contenteditable='false' class='address-placeholder'></span>");

        ////////// reinsert placeholder text in span
        $('.address-placeholder').text(placeholder_text);

        ////////// append message in input after span node
        $('.address-placeholder').after(message);

    }

});






//var data = $('#alertList').data('alertlist');

//                '<div><p>from the image</p></div>',
//                '<div><img class="captcha-img" src="'+data['url']+'"></div>',
//                '<div><input type="text" class="captcha-input"></div>',
//                '<div><button id="captcha-button">submit</button></div>'
//                '<div class="captcha-alert"></div>',
//                '<div hidden id="emailData" data-emailData="'+stringJson+'"></div>',
//                '<div hidden class="captcha-uid">'+ data['uid'] +'</div>





function setEndOfContenteditable(contentEditableElement)
{
    var range,selection;
    if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
    {
        range = document.createRange();//Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(contentEditableElement[0]);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection();//get the selection object (allows you to change selection)
        selection.removeAllRanges();//remove any selections already made
        selection.addRange(range);//make the range you have just created the visible selection
    }
    else if(document.selection)//IE 8 and lower
    {
        range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
        range.moveToElementText(contentEditableElement[0]);//Select the entire contents of the element with the range
        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
        range.select();//Select the range (make it the visible selection
    }
}

function updateTextCount() {
    var user_entered_text = $('#text-input').text().slice(
        $('.address-placeholder').eq(0).text().length);
    count_remaining = 280 - twttr.txt.getTweetLength(
        get_longest_address() + " " + user_entered_text + site_url_to_append);
    $('.letter-count').text(count_remaining);
    $('.letter-count').css({'color': count_remaining < 0 ? 'red' : 'gray'});
}


function get_longest_address(){
    var longestAddressLength = 0;
    var longest_address = "";
    $('.address-item-label:visible').each(function(){
        var text = $(this).text();
        if (text.length > longestAddressLength){
            longestAddressLength = text.length;
            longest_address = text;
        }
    });
    return longest_address;
}


site_url_to_append = '';
$(document).ready(function () {
    $(document).on('change', '#twitter_input_add_url', function () {
        if ($(this).prop('checked')) {
            site_url_to_append = ' https://www.pushthought.com/' +
                window.location.href.split('/').slice(3).join('/');
        } else {
            site_url_to_append = '';
        }
        updateTextCount();
    })
    $('#twitter_input_add_url').change();
});


function showLoadingForSelectedMembers() {
    $('.action-panel-container.selected').each(function() {
        $('.loader-' + this.id).show();
    });
    $('.tweet-loader').show();
}


function hideLoading() {
    $('.loader').hide();
    $('.tweet-loader').hide();
}


function close_form() {
    $('.copy-last').hide();
    $('#text-input').text('');
    $('.letter-count').show();
    $('.email-action-container').hide();
    $('#required-fields-label').hide();
    $('.warning-text').hide();
    $('.address-placeholder').html('');
    $('.address-container').html(' ');
//    $('.category-container').animate({'height':'220px'});
//    $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
//        $('.rep-action-container').css('display','none');
//    });
//    $('.rep-color-band').animate({'height':'220px'},500,function() {});
//    $('.rep-color-band').animate({'height':'253px'});

    $('.rep-action-container')
        .addClass('hiding')
        .animate({'opacity':'0.0'},500,function() {
            $('.rep-action-container')
                .css('display','none')
                .removeClass('hiding');
        });

    $('#text-input').animate({'height':'100px','max-height':'100px'});


    //$('.twitter-icon').animate({'left':'42%'});
    $('.selected').removeClass('selected');
    $('#img-send-email-icon').hide();
    $('#img-send-tweet-icon').show();
    $('#email-button-label').hide();
    $('#twitter-button-label').show();


    focus_on_text_input();
}
