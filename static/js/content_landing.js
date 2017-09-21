//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");

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
    $('.submit-zip').click( function() {
        // validators
        var zip = $('.zip-input').val();
        var isValidZip = /(^\d{5}$)/.test(zip);

        if (isValidZip){
            $('#zip-loader').show();
            console.log('valid zip');
            console.log('get_congres on zip:' + zip);
            $('.zip-input').attr('id',zip);
            $('.zip-input').attr('value',zip);
            get_congress(zip);
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


//     auto trigger email icon
//    setTimeout(function(){ $('.zip-reset').trigger('click'); }, 400);

    // If alerts, scroll down and show them
    var data = $('#alertList').data('alertlist');
    if(data){
        console.log("alert list is present");
        for (var i = 0; i < data.length; i++) {
            alertArray.push(data[i]);
        }
    } else {
        console.log("alert list is empty");
    }

//    alertArray = JSON.parse(data);
    alertArray = [];




    // Alerts if @symbols in tweet and went through verify catch redirect
    if (alertArray[0]){
        // scroll down
        var headerAllowance = $('.seen-it-container').offset().top - 20;
        $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        showSuccess(alertArray[0], alertArray[1]);
    }

    // Alerts if no @ message and went through verify-catch redirect
    if(alertArray[3] == true){
        alert("Tweet is over 140 characters. Shorten a few characters and try again.");
    } else if(alertArray[4] == true){
        alert("Your tweet has been sent.");
    } else if(alertArray[5] == true){
        alert("Message is duplicate on your twitter account.  Please alter your message and try again.");
    } else if(alertArray[6]){
        alert("There has been an error with twitter.  Please check message and try again.  If it persists, notify Push Thought");
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
        $('.rep-action-container').css('display','block'),400,function(){
        };

        // scroll to appropriate place on screen to see action container
//        $('.category-container').animate({'height':'350px'},200,function(){
//            var headerAllowance = $('.seen-it-container').offset().top - 20;
//            $('html, body').animate({
//                scrollTop: headerAllowance + 'px'
//            }, 'fast');
//        });

        // expand containers
        $('#text-input').animate({'height':'200px','max-height':'200px'});
//        $('.rep-color-band').animate({'height':'850px'}); //220
//        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});
        $('.rep-action-container').animate({'opacity':'1.0'});
        $('.rep-action-container').animate({'display':'block'});



        // hide items that need to disappear
        $('.twitter-icon').hide();
        $('.twitter-icon-empty').hide();
        $('.phone-icon').hide();
        $('.email-icon').hide();
        $('.email-icon-gray').hide();

        // show email name selected, hide others
        $('#'+i+'.email-name').show();

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


         // insert address placeholder in text-input
        var addressPlaceholderClass = '.address-item-label-' + i;
        var addressPlaceholder = $(addressPlaceholderClass).text();
        addressPlaceholder = String(addressPlaceholder);

        console.log("address placeholder: ", addressPlaceholder);
        $('#text-input').html('<span contenteditable=false class="address-placeholder">Congressperson '+  addressPlaceholder +',</span><p class="space-placeholder" style="display:inline;"> </p>');
        console.log($('#text-input').html());


        // select address according to button clicked
        $(".address-node-" + i).toggleClass("selected");

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


        //setEndOfContenteditable($('#text-input'));
        updateTextCount();


        // grab BioguideID and reqeust congress phantom email fields from server
        var bioguideId = $(this).next().attr('id');

        //get fields from db or phantom congress
        var bioguideArray = bioguideId
        // alert (bioguideArray)
        // var bioguideArray = [];
        // $('.bioguide-mule').each(function(){
        //     var bioguideId = $(this).attr('id');
        //     bioguideArray.push(bioguideId);
        // });
        //console.log("bioguide sending to email phantom congress to get email fields: "+bioguideArray);
        //$.getScript('/static/js/content_landing_email_action.js', function(){
            get_congress_email_fields(bioguideArray);
        //});

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
    });
        // Focus on text box
        $('#text-input').focus();

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
//        $('.category-container').animate({'height':'350px'},200,function(){
//            var headerAllowance = $('.seen-it-container').offset().top - 20;
//            $('html, body').animate({
//                scrollTop: headerAllowance + 'px'
//            }, 'fast');
//        });

        // expand containers
//        $('.rep-color-band').animate({'height':'455px'});
//        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});
        $('.rep-action-container').animate({'opacity':'1.0'});
        $('.rep-action-container').animate({'display':'block'});

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


        // select or toggle selection of activity container
        $('.action-panel-container#'+i).addClass("selected");

        // create address items above text input
        $('.twitter-name').each(function( index ){
           index = index + 1; //add 1 because this index starts at 0 as where HTML forloop it matches starts at 1
           var address = $(this).text();
           var bioguideId = $(this).attr('name');
           //console.log(bioguideId);
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
        $('#text-input').html('<span contenteditable=false class="address-placeholder">'+addressPlaceholder+'</span><p class="space-placeholder" style="display:inline;"> </p>');

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems;
        $('#tweet-button-label').text(labelText);

        // Focus on text box
        if($(window).width() < 525){
            console.log("no focus, width low");
        } else {
            //console.log("focus, width high");
            $('#text-input').focus();
            //setEndOfContenteditable($('#text-input'));
        }
        updateTextCount();
        $('#text-input').focus();
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
        $('.letter-count').show();
        $('.email-action-container').html('');
         $('#required-fields-label').hide();
        $('.warning-text').hide();
        $('.address-placeholder').html('');
        $('.address-container').html(' ');
//        $('.category-container').animate({'height':'220px'});
//        $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
//            $('.rep-action-container').css('display','none');
//        });
//        $('.rep-color-band').animate({'height':'220px'},500,function() {});
//        $('.rep-color-band').animate({'height':'253px'});

        $('.rep-action-container').animate({'opacity':'0.0'},500,function() {
            $('.rep-action-container').css('display','none');
        });

        $('#text-input').animate({'height':'100px','max-height':'100px'});


        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').show();
        $('.twitter-icon-empty').show();
        $('.phone-icon').show();
        $('.email-icon').show();
        $('.email-icon-gray').show();
        $('.twitter-name').hide();
        $('.email-name').hide();
        $('.selected').removeClass('selected');
        $('#img-send-email-icon').hide();
        $('#img-send-tweet-icon').show();
        $('#email-button-label').hide();
        $('#twitter-button-label').show();


        $('#text-input').focus();
    });

    // Action Panel Container
    $('.rep-container').on("click", ".action-panel-container", function(e) {

        //////////////////////////////////////
        // get number of action panel clicked
        //////////////////////////////////////
        var i = $(this).attr('id');

        //////////////////////////////////////////////////////
        // get twitter name if twitter names visible
        //////////////////////////////////////////////////////
        if($('.twitter-name').is(":visible")){
            var elementRef = "#email-name-"+i;
            var elementText = $('#twitter-name-'+i).text();
            var whichIconClicked = "tweet";
        ////////////////////////////////////////////////////////////
        // if email visible and class 'selected' exists, then close
        ////////////////////////////////////////////////////////////
        } else if($('.email-name').is(":visible")){
            var whichIconClicked = "email";
            if($(this).hasClass('selected')){
                $('#close-button').trigger('click');
                console.log("email should close");
            ////////////////////////////////////////////////////////////
            // if email visible and class NOT 'selected' then alert
            ////////////////////////////////////////////////////////////  v
            } else {
                var elementText = $('div#'+i+'.email-name').text();
                alert("Currently you can only email 1 representative at a time.  Autofill will help you fill out consecutive emails.");
            }

            return false;
        } else {
            return false;
        }

        ///////////////////////////////////////////////////////
        // to make it here, tweet name visible is only option,
        // check if tweet name exists, if not, then alert
        ///////////////////////////////////////////////////////
        if( elementText == 'n/a'){
            alert('Don\'t have this item yet.  We\'re working on it.  Thank you for your patience.');
            return false;
        ///////////////////////////////////////////////////////
        // Twitter name has value!
        // switch status to selected or unselected based on
        // current state.  change state of address node above input
        ///////////////////////////////////////////////////////
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

            ///////////////////////////////////////////////////////////
            // grabbing length of placeholder text and value of #textInput
            ///////////////////////////////////////////////////////////
            var placeholderLength = $('.address-placeholder').text().length
            value = $('#text-input').html();
            console.log("placeholder length: " + placeholderLength);
            console.log("html value: " + value);

            ///////////////////////////////////////////////////
            // add placeholder if one does not exist
            //////////////////////////////////////////////////
            searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
            if (searchBool == -1){
                console.log("there is no placeholder");
                $('#text-input').html(value + '<span contenteditable=false class=address-placeholder></span><p> class="space-placeholder" style="display:inline;"> </p>');
            }

            // Get count of selected items
            var numItems = $('.address-item.selected').length;

            console.log("number of items: "+numItems);
            // Change button label
            if (whichIconClicked == "email"){
              console.log("this code should never trigger, change button label email");
              var labelText = 'email: ' + numItems;
              $('#email-button-label').text(labelText);
            } else{
              var labelText = 'tweet: ' + numItems;
              $('#tweet-button-label').text(labelText);
            }

            // EMAIL - hide / show fields
            //if($('.email-name').is(":visible")){

                /*$('.email-form-field-container').hide();
                var showArray = []
                $('.address-item-label:visible').each(function(){
                    var bioguideId = $(this).attr('id');
                    showArray.push(bioguideId);
                });
                console.log(showArray);
                for (var i = 0; i < showArray.length; i++) {
                    $('.'+ showArray[i]).show();
                }*/


            // TWEET - adjust placeholder text
            //} else{
                // update placeholderText -> based on # of addresses selected
                if (numItems == 0){
                    placeholderText = '';
                    $('.address-placeholder').text(placeholderText);
                } else if (numItems == 1){
                    placeholderText = $('.address-item.selected').children('p').html();
                    placeholderText = placeholderText + '';
                    $('.address-placeholder').text(placeholderText);
                } else {
                    placeholderText = '@multiple';
                    placeholderText = placeholderText + ''; // endspace important so @ recognized
                    $('.address-placeholder').text(placeholderText);
                }
            //}
        }
        //$('#text-input').focus();
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
        searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
        if (searchBool == -1){

            ////////////////////////////////////////////////////////
            // if twitter visible, then replace address placeholder
            /////////////////////////////////////////////////////////

            if($('.twitter-name').is(":visible")){
                $('#text-input').html('<span contenteditable=false class=address-placeholder></span><p class="space-placeholder" style="display:inline;"> </p>' + value);
                console.log("text-input-html 2: " + $('#text-input').html());

                ////////////////////////////////////////////////////////
                // remove all selected action containers
                /////////////////////////////////////////////////////////
                $('.action-panel-container').each(function(){
                     if ($(this).hasClass( "selected" )){
                        $(this).removeClass('selected');
                     }
                });

                ////////////////////////////////////////////////////////
                // remove all selected address items
                /////////////////////////////////////////////////////////
                $('.address-item').each(function(){
                     if ($(this).hasClass( "selected" )){
                        $(this).removeClass('selected');
                     }
                });

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
            countSelected = 0;
            if($('.email-name').is(":visible")){
                var email_name = $('.email-name:visible').attr('name');
                 $('#text-input').html('<span contenteditable=false class=address-placeholder>Congessperson ' + email_name + ',</span><p class="space-placeholder" style="display:inline;"> </p>' + value);
                 $('.email-name:visible').parent().parent().addClass('selected');
                countSelected = countSelected + 1;
                var labelText = 'email: ' + countSelected;
                $('#email-button-label').text(labelText);
            } else {
                var labelText = 'tweet: ' + countSelected;
                $('#tweet-button-label').text(labelText);
            }
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

//        console.log("addressInput:", addressInput);
//        console.log("countAddressInput:", countAddressInput);
//        console.log("countTextInput:", countTextInput);
//        console.log("longestAddressLength:", longestAddressLength);
//        console.log("countRemaining:", countRemaining);

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

        // loop through and find longest address
    function get_longest_address(){
        var longestAddressLength = 0;
        $('.address-item-label:visible').each(function(){
            var text = $(this).text();
            if (text.length > longestAddressLength){
                longestAddressLength = text.length;
            }
        });
        return longestAddressLength;
    }

    // TWEET/EMAIL Button
    $('#tweet-button').on('click',function(event) {


        if($('.email-name').is(":visible")){
            // alert("Under development");
            var bioguideId = $('.address-item-label:visible').attr('id');
            // console.log("printing bioguide before run email", bioguideId);
            console.log("email/tweet button initializing email send");

            // for each eform class make add to dictionary
            // keys are id truncated
            //values are eform .val()
            // store dictionary in session
            // by pinging server


            //updateEmailFieldsInSession();

            runEmail(bioguideId);
        } else {
            runTweet(windowURL);
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


    $('.hashtag-container').on("click", ".hashtag-item", function(e) {
        // Function: Select text of tweet
        function SelectText(element) {
            var doc = document;
            var text = element;
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

        // Copy hashtag text to Clipboard
        var element = $(this).contents('.hashtag-item').contents().filter(function () { return this.nodeType === 3; });
        SelectText(element);
        document.execCommand("copy");

        // Show Copy to Clipboard indicator
        var element = $(this).contents('#copied-to-clipboard')
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

        // Function: Select text of tweet
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

        // Copy tweet text to Clipboard
        var element = $(this).contents('.tweet').contents().filter(function () { return this.nodeType === 3; });
        SelectText(element);
        document.execCommand("copy");

        // Show Copy to Clipboard indicator
        var element = $(this).contents('#copied-to-clipboard')
        element.show();
        element.animate({"height":"47"},400,function(){
            setTimeout(function(){
                element.animate({"height":"0"},400,function(){
                    element.hide();
                });
             }, 400);
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





//function setEndOfContenteditable(contentEditableElement)
//{
//    var range,selection;
//    if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
//    {
//        range = document.createRange();//Create a range (a range is a like the selection but invisible)
//        range.selectNodeContents(contentEditableElement[0]);//Select the entire contents of the element with the range
//        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
//        selection = window.getSelection();//get the selection object (allows you to change selection)
//        selection.removeAllRanges();//remove any selections already made
//        selection.addRange(range);//make the range you have just created the visible selection
//    }
//    else if(document.selection)//IE 8 and lower
//    {
//        range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
//        range.moveToElementText(contentEditableElement[0]);//Select the entire contents of the element with the range
//        range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
//        range.select();//Select the range (make it the visible selection
//    }
//}
