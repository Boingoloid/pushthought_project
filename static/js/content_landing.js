




//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");




$(document).ready(function() {
    setTimeout(function(){ $('#email-icon-3').trigger('click'); }, 400);

    // If alerts, scroll doewn and show them
    var data = $('#alertList').data('alertlist');
    if(data){
        var headerAllowance = $('.seen-it-container').offset().top - 20;
        $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        console.log(data);
        showSuccess(data[0], data[1]);
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
//        $('.submit-zip').show();

    });


    $('.location-icon').click(function(){
        alert("Still in Development: Our location finder is being built, please enter you zip using the box below.  We'll move the cursor there for you :)");
        $('.zip-input').focus();
    });

    $('.zip-input').focusin(function(){
        $('.submit-zip').show();
    });


    // show/hide zip submit button if focus on zip-input
    $(document).mouseup(function(){
        if ($('.zip-input') == "focused"){
            $('.submit-zip').show();
        } else{
            if($(".submit-zip:visible").length==1){
                $(".submit-zip").hide(); // Toggle
            }
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


    // Zip submission button click
    $('.submit-zip').click( function() {
        // validators
        var zip = $('.zip-input').val();
        var isValidZip = /(^\d{5}$)/.test(zip);

        if (isValidZip){
            $('#zip-loader').show();
            console.log('valid zip');
            console.log('get_congres on zip:' + zip);
            $.getScript('/static/js/content_landing_get_congress.js', function(){
                get_congress(zip);
            });
        } else{
            console.log('NOT a valid zip');
            alert('Not a valid zip code.  Please check and try again.')
            $('.zip-input').focus();
            $(this).show();
        }
    });

    // Watch button
    $('.watch-button').click( function() {
       //var idText = $(this).attr('id');
       //var repIndex = idText.replace('program-item','');
       //var programObjectIdElementName = "#program-item-objectId" + repIndex;
       //var programObjectId = $(programObjectIdElementName).text();
       window.location.href="/leaving";
    });


    // Email Icon
    $('.rep-container').on("click", "img.email-icon", function(e) {
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
        if ($(':animated').length > 0) {
            return false;
        }

        // show action container and it's contents
        $('.rep-action-container').css('display','block'),200,function(){
        };

        // scroll to appropriate place on screen to see action container
        $('.category-container').animate({'height':'350px'},200,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });

        // expand containers
        $('.rep-color-band').animate({'height':'850px'}); //220
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});


        // hide items that need to disappear
        $('.twitter-icon').hide();
        $('.twitter-icon-empty').hide();
        $('.phone-icon').hide();
        $('.email-icon').hide();
        $('.email-icon-gray').hide();

        // show email name
        $('.email-name').show();

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

        // text-input clear
        $('#text-input').html('');
        $('.address-placeholder').html('');

        // insert address placeholder in text-input
        stringSpace = '&nbsp';
        $('#text-input').html('<span contenteditable=false class=address-placeholder></span>');

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

        // Focus on text box
        $('#text-input').focus();
        updateTextCount();


        // grab BioguideID and reqeust congress phantom email fields from server
        var bioguideId = $(this).next().attr('id');

        //get fields from db or phantom congress
        var bioguideArray = [];
        $('.bioguide-mule').each(function(){
            var bioguideId = $(this).attr('id');
            bioguideArray.push(bioguideId);
        });
        console.log("bioguide:"+bioguideArray);
        $.getScript('/static/js/content_landing_email_action.js', function(){
            get_congress_email_fields(bioguideArray);
        });

    });


    // Twitter Icon
    $('.rep-container').on("click", "img.twitter-icon", function(e) {
        e.stopPropagation();
        var i = $(this).attr('id');

        // if animation occuring, stop method
        if ($(':animated').length > 0) {
            console.log("returning false");
            return false;
        };

        // show action container
        $('.rep-action-container').show();

        // scroll to appropriate place on screen to see action container
        $('.category-container').animate({'height':'350px'},200,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });

        // expand containers
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});

        // hide icons that disappear
        $('.twitter-icon').hide();
        $('.twitter-icon-empty').hide();
        $('.phone-icon').hide();
        $('.email-icon').hide();
        $('.email-icon-gray').hide();

        // show twitter name
        $('.twitter-name').show();

        // show Send button and label , hide Email button and label
        $('.img-send-tweet-icon').show();
        $('.tweet-button-label').show();
        $('.email-button-label').hide();
        $('.img-send-email-icon').hide();

        // toggle selection of activity container
        $('.action-panel-contianer#'+i).toggleClass('selected');  //WHY THE FUCK IS THIS CONTIANER, I DONT GET IT!!!

        // create address items above text input
        $('.twitter-name').each(function( index ){
           index = index + 1; //add 1 because this index starts at 0 as where HTML forloop it matches starts at 1
           var address = $(this).text();
           var text = ['<div class="address-item address-node-'+ index +'">',
                            '<p class="address-item-label address-item-label-'+index +'">'+address+'</p>',
                      '</div>'].join("\n");
           $('.address-container').append(text);
        });

        // select address according to button clicked
        console.log(".address-node-" + i);
        $(".address-node-" + i).toggleClass("selected");


        // insert address placeholder in text-input
        var addressPlaceholderClass = '.address-item-label-' + i;
        var addressPlaceholder = $(addressPlaceholderClass).text();
        addressPlaceholder = String(addressPlaceholder + ' '); // Space important! allows @ to be recognized
        $('#text-input').html('<span contenteditable=false class="address-placeholder">'+addressPlaceholder+'</span>');

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems;
        $('#tweet-button-label').text(labelText);

        // Focus on text box
        $('#text-input').focus();
        updateTextCount();
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

    $('#close-button').on('click',function(event) {
        $('#text-input').text('');
        $('.email-action-container').html('');
        $('.address-placeholder').html('');
        $('.address-container').html(' ');
        $('.category-container').animate({'height':'220px'});
        $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
            $('.rep-action-container').css('display','none');
        });
        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').show();
        $('.twitter-icon-empty').show();
        $('.phone-icon').show();
        $('.email-icon').show();
        $('.email-icon-gray').show();
        $('.twitter-name').hide();
        $('.email-name').hide();
        $('.rep-color-band').animate({'height':'233px'});
        $('.selected').animate($('.selected').removeClass('selected'));
        $('#img-send-email-icon').hide();
        $('#img-send-tweet-icon').show();
        $('#email-button-label').hide();
        $('#twitter-button-label').show();


    });

    // Action Panel Container
    $('.rep-container').on("click", ".action-panel-container", function(e) {
        var i = $(this).attr('id');
        // get either twitter name or email value, depending on which is visible.
        if($('.twitter-name').is(":visible")){
            var whichIconClicked = "twitter";
            var elementRef = "#email-name-"+i;
            var elementText = $('#twitter-name-'+i).text();
        } else if($('.email-name').is(":visible")){
            var whichIconClicked = "email";
            var elementText = $('div#'+i+'.email-name').text();
        } else {
            return false;
        }

        // If no item, then return false
        if( elementText == 'n/a'){
            alert('Don\'t have this item yet.  We\'re working on it.  Thank you for your patience.');
            return false;
        //else label container as selected
        } else {
            // adjust the highlight of selected/unselected container
            if ($(this).hasClass( "selected" )){
                $(this).removeClass('selected');
                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-node-" + index;
                $(addressPath).removeClass('selected');
            } else {
                $(this).addClass('selected');
                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-node-" + index;
                $(addressPath).addClass('selected');
            }

            // grapping length and value of textInput and placeholder
            var placeholderLength = $('.address-placeholder').text().length
            value = $('#text-input').html();

            // add placeholder if one does not exist
            searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
            if (searchBool == -1){
                $('#text-input').html(value + '<span contenteditable=false class=address-placeholder></span>');
            }

            // Get count of selected items
            var numItems = $('.address-item.selected').length;

            //console.log("number of items: "+numItems);
            // Change button label
            if (whichIconClicked == "email"){
              var labelText = 'email: ' + numItems;
              $('#email-button-label').text(labelText);
            } else{
              var labelText = 'tweet: ' + numItems;
              $('#tweet-button-label').text(labelText);
            }

            // EMAIL - hide / show fields
            if($('.email-name').is(":visible")){

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


            // TWEET - adjust placeholder text
            } else{
                // update placeholderText -> based on # of addresses selected
                if (numItems == 0){
                    placeholderText = '';
                    $('.address-placeholder').text(placeholderText);
                } else if (numItems == 1){
                    placeholderText = $('.address-item.selected').children('p').html();
                    placeholderText = placeholderText + ' ';
                    $('.address-placeholder').text(placeholderText);
                } else {
                    placeholderText = '@multiple';
                    placeholderText = placeholderText + ' '; // endspace important so @ recognized
                    $('.address-placeholder').text(placeholderText);
                }
            }
        }
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



    // Key Up: replaces placeholder if missing, updates count, updates selected
    $('#text-input').keyup(function() {
        // count letters and update letter count
        updateTextCount();

        // If Placeholder changed, update selections and button label
        var value = $('#text-input').html();
        var placeholderLength = $('.address-placeholder').text().length;
        searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
        if (searchBool == -1){
            //console.log("span is NOT there, adding");
            $('#text-input').html('<span contenteditable=false class=address-placeholder></span>' + value);
            $('.action-panel-container').each(function(){
                 if ($(this).hasClass( "selected" )){
                    $(this).removeClass('selected');
                 }
            });
            $('.address-item').each(function(){
                 if ($(this).hasClass( "selected" )){
                    $(this).removeClass('selected');
                 }
            });

            // set button label
            countSelected = 0;
            $('.address-item').each(function(){
                if($(this).hasClass('selected')){
                    countSelected = countSelected + 1;
                }
            });

            if($('.email-name').is(":visible")){
                var labelText = 'email: ' + countSelected;
                $('#email-button-label').text(labelText);
            } else {
                var labelText = 'tweet: ' + countSelected;
                $('#tweet-button-label').text(labelText);
            }
        }
    });



    function updateTextCount(){
        var textInput = $('#text-input').text();
        var twitterMax = 140;
        var twitterDefaultLinkLength = 22;
        var countAfterLink = twitterMax - twitterDefaultLinkLength;

        var addressInput = $('.address-placeholder').text();
        var countAddressInput =  addressInput.length;
        var countTextInput =  textInput.length;
        var longestAddressLength = get_longest_address();
        var countRemaining = countAfterLink - countTextInput + countAddressInput - longestAddressLength;

        // adjust for line breaks
        numberOfLineBreaks = (textInput.match(/\n/g)||[]).length;
        countRemaining = countRemaining - numberOfLineBreaks;

        $('.letter-count').text(countRemaining);
        if (countRemaining < 0){
            $('.letter-count').css({'color':'red'});
        } else {
            $('.letter-count').css({'color':'gray'});
        }
    }


    $('#tweet-button').on('click',function(event) {
        if($('.email-name').is(":visible")){
            var bioguideId = 'F000062';
            console.log("tweet button initializing email send");
//            $.getScript('/static/js/content_landing_email_action.js'), function (){
                runEmail(bioguideId);
//            };
        } else {
            runTweet();
        }
    });






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

});

//var data = $('#alertList').data('alertlist');

//                '<div><p>from the image</p></div>',
//                '<div><img class="captcha-img" src="'+data['url']+'"></div>',
//                '<div><input type="text" class="captcha-input"></div>',
//                '<div><button id="captcha-button">submit</button></div>'
//                '<div class="captcha-alert"></div>',
//                '<div hidden id="emailData" data-emailData="'+stringJson+'"></div>',
//                '<div hidden class="captcha-uid">'+ data['uid'] +'</div>





