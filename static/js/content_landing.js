




//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");




$(document).ready(function() {


    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
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




    $(document).on('paste','[contenteditable]',function(e) {
        e.preventDefault();
        var text = (e.originalEvent || e).clipboardData.getData('text/plain');
        window.document.execCommand('insertText', false, text);
    });


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

    $('.action-panel-container').mouseenter(function() {
        if($("#text-input:visible").length==1){
            $(this).css({"cursor": "pointer"});
        }
    });

    $('.action-panel-container').mouseleave(function() {
        $(this).css({"cursor": "default"});
    });

    $('.zip-indicator').mouseenter(function() {
        $('.zip-reset').show();
      });

    $('.zip-reset-hover-boundary').mouseleave(function() {
        $('.zip-reset').hide();
    });

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
    });

    $('.location-icon').click(function(){
        alert("Still in Development: Our location finder is being built, please enter you zip using the box below.  We'll move the cursor there for you :)");
        $('.zip-input').focus();
    });


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

    $(document).mouseup(function(){
        if ($('.zip-input') == "focused"){
            $('.submit-zip').show();
        } else{
            if($(".submit-zip:visible").length==1){
                $(".submit-zip").hide(); // Toggle
            }
        }
    });


//    get_congress();


   $('.submit-zip').click( function() {
        // validators
        var zip = $('.zip-input').val();
        var isValidZip = /(^\d{5}$)/.test(zip);

        if (isValidZip){
            $('#zip-loader').show();
            console.log('valid zip');
            console.log('get_congres on zip:' + zip);
            get_congress(zip);

        } else{
            console.log('NOT a valid zip');
            alert('Not a valid zip code.  Please check and try again.')
            $('.zip-input').focus();
            $(this).show();

        }

    });

//    Object.prototype.getName = function() {
//       var funcNameRegex = /function (.{1,})\(/;
//       var results = (funcNameRegex).exec((this).constructor.toString());
//       return (results && results.length > 1) ? results[1] : "";
//    };

    var data = $('#alertList').data('alertlist');
    if(data){
        var headerAllowance = $('.seen-it-container').offset().top - 20;
        $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        console.log(data);
        showSuccess(data[0], data[1]);
    }





    $('.watch-button').click( function() {
       //var idText = $(this).attr('id');
       //var repIndex = idText.replace('program-item','');
       //var programObjectIdElementName = "#program-item-objectId" + repIndex;
       //var programObjectId = $(programObjectIdElementName).text();
       window.location.href="/leaving";
    });

    $('.rep-container').on("click", "img.email-icon", function() {
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

        // grab BioguideID and reqeust congress phantom email fields from server
        var bioguideId = $(this).next().attr('id');
        //console.log(bioguideId);
        get_congress_email_fields(bioguideId);  //get fields from db or phantom congress

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
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});

        // hide items that need to disappear
        $('.twitter-icon').css('display','none');
        $('.twitter-icon-empty').css('display','none');
        $('.phone-icon').css('display','none');
        $('.email-icon').css('display','none');
        $('.email-icon-gray').css('display','none');

        // show email name
        $('.email-name').show();

        // select or toggle selection of activity container
        $('.action-panel-contianer').toggleClass("selected");  //WHY THE FUCK IS THIS CONTIANER, I DONT GET IT!!!

        //        // toggle address paths above text input
        //        var index = $(this).parent('div').parent('div').attr('id');
        //        var addressPath = ".email-address-item-" + index;
        //        $(addressPath).toggleClass('selected');


        // create address items above text input
        $('.email-name').each(function( index ){
            //           console.log("index:" + index);
           if(i == index){
                //console.log('yes');
           }
           var full_name = $(this).attr('name');
           var text = ['<div class="address-item address-node-'+ index +'">',
                            '<p class="address-item-label address-item-label-'+index +'">'+full_name+'</p>',
                      '</div>'].join('\n');
           $(".address-container").append(text);
        });


        // select address according to button clicked
//        var addressPath = String(".address-node-" + i);
        console.log('Before address node lookup: check 9991');
        $(".address-node-" + i).toggleClass("selected");

        // text-input clear
        $('#text-input').html('');
        $('.address-placeholder').html('');


        // show Send button , hide Tweet button
        $('#img-send-tweet-icon').hide();
        $('#tweet-button-label').hide();
        $('#img-send-email-icon').show();
        $('#email-button-label').show();

        countSelected = 0;
        $('.address-item').each(function(){
            if($(this).hasClass('selected')){
                countSelected = countSelected+1;
                console.log('yes');
            }

        });
        console.log('countSelected:'+countSelected);

        var labelText = 'email: ' + countSelected;
        console.log(labelText);

        $('#email-button-label').text(labelText);


//        // set button label
//        var numItems;
        var x = document.getElementsByClassName(".address-item.selected").length;
        console.log("x:"+x);
//        var labelText = 'email: ' + numItems;
//        console.log('label text: ' + labelText);
//        $('#email-button-label').show();
//        $('#email-button-label').text(labelText);
//        $('#tweet-button-label').hide();

        // Focus on text box
        $('#text-input').focus();

    });



    $('.rep-container').on("click", "img.twitter-icon", function() {
        var i = $(this).attr('id');
        console.log("i:" + i);

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

        // hide items that disappear
        $('.twitter-icon').css('display','none');
        $('.twitter-icon-empty').css('display','none');
        $('.phone-icon').css('display','none');
        $('.email-icon').css('display','none');
        $('.email-icon-gray').css('display','none');

        // show twitter name
        $('.twitter-name').show();

        // toggle selection of activity container
        $('.action-panel-contianer#'+i).toggleClass('selected');  //WHY THE FUCK IS THIS CONTIANER, I DONT GET IT!!!

        // create address items above text input
        $('.twitter-name').each(function( index ){
           index = index + 1;
           //console.log("index:" + index);
           if(i == index){
                console.log('yes');
           }

           var address = $(this).text();
           var text = ['<div class="address-item address-node-'+ index +'">',
                            '<p class="address-item-label address-item-label-'+index +'">'+address+'</p>',
                      '</div>'].join("\n");
           $('.address-container').append(text);
        });

        // select address according to button clicked
        var addressPath = String(".address-node-" + i);
        console.log(addressPath);
        $(addressPath).toggleClass("selected");

        // insert address placeholder in text-input
        addressPlaceholderClass = '.address-item-label-' + i;
        addressPlaceholder = $(addressPlaceholderClass).html();
        stringSpace = '&nbsp';
        $('#text-input').html('<span contenteditable=false class=address-placeholder>' + addressPlaceholder + '</span>');

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems;
        $('#tweet-button-label').text(labelText);

        // Focus on text box
        $('#text-input').focus();



        //var tweetText = $('#text-input').text();
        //letterCount = tweetText.length;
        //console.log("letter count:" + letterCount);



        //range = window.getSelection().getRangeAt(0);
        //range.setStart(range.endContainer,range.endOffset);
        //document.execCommand('selectAll',false,null);
        //console.log(window.getSelection().getRangeAt(0));
        //var selection = window.getSelection();

        //selection.focusOffset = 3;
        //selection.focus(3);
        //console.log("selection.focusNode.data[selection.focusOffset]" + selection.focusNode.data[selection.focusOffset]);
        //        alert(selection.focusOffset);
        //var index = tweetText.indexOf()
        //document.selection.select
    });

    $('.rep-container').on("click", "img.twitter-icon-empty", function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        }
        $('.warning-box-tweet-icon').css({'opacity':'1'});
        $('.warning-box-tweet-icon').animate({'opacity':'0.0'},2500,function() {});
    });

    $('.rep-container').on("click", "img.phone-icon", function() {
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



    $('.rep-container').on("click", "img.email-icon-gray", function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        alert('sorry, no email form yet for this person.  Pleaes call or tweet.');
    });

    $('#close-button').on('click',function(event) {
        $('#text-input').text('');
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


    $('.rep-container').on("click", ".action-panel-container", function() {
        var i = $(this).attr('id');
        console.log("i:"+i);
        // get either twitter name or email value, depending on which is visible.
        if($('.twitter-name').is(":visible")){
            var whichIconClicked = "twitter";
            var elementRef = "#email-name-"+i;
            console.log(elementRef);
            var elementText = $('#twitter-name-'+i).text();
            console.log("twitter element Text: "+ elementText);
        } else if($('.email-name').is(":visible")){
            var whichIconClicked = "email";
            var elementText = $('div#'+i+'.email-name').text();
            console.log("email element Text: "+ elementText);
        } else {
            return false;
        }

        if( elementText == 'n/a'){
            alert('Don\'t have this item yet.  We\'re working on it.  Thank you for your patience.');
            return false;
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

            // grapping length and value of textInput
            var placeholderLength = $('.address-placeholder').text().length
            value = $('#text-input').html();

            // add placeholder if one does not exist
            searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
            if (searchBool == -1){
                $('#text-input').html(value + '<span contenteditable=false class=address-placeholder></span>');
            }

            // Get count of selected items
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



            // update placeholderText -> based on # of addresses selected

            if (numItems == 0){
                placeholderText = '';
                $('.address-placeholder').text(placeholderText);
            } else if (numItems == 1){
                placeholderText = $('.address-item.selected').children('p').html();
                $('.address-placeholder').text(placeholderText);
            } else {
                placeholderText = '@multiple';
                $('.address-placeholder').text('@multiple');
            }


        }
    });

    $('#clear-button').on('click',function(event) {
        var addressPlaceholder = $('.address-placeholder').text();
        console.log(addressPlaceholder);
        $('#text-input').html('<span contenteditable=false class=address-placeholder>' + addressPlaceholder + '</span>');
    });

    $('#img-checked-box').on('click',function(event) {
        if ($(':animated').length) {
            console.log("cancelling click");
            return false;
        }
        //alert('The link is always included for context')
        $('.warning-box').css({'opacity':'1'});
        $('.warning-box').animate({'opacity':'0.0'},2500,function() {
        });
    });

    var window_url =  window.location.href;
    var segment_id = $('#segmentId').text();
    var program_id = $('#programId').text();


   $('#tweet-button').on('click',function(event) {

      // get tweet and validate length
      var tweet_text = $('#text-input').text();
      if(tweet_text.length < 1){
        alert ("Please type a message to tweet first");
      } else {

        //
        addressArray = [];
        $('.action-panel-container.selected').each(function() {
            index = $(this).attr('id');
            function showLoading(index){
                var loaderDiv = '.loader-' + index;
                $(loaderDiv).show();
                $('.tweet-loader').show();
            }
            showLoading(index);

            twitterName = $(this).contents().contents('.twitter-name').text();
            addressArray.push(twitterName);
         });
        // create dataSet string
        dataSet = JSON.stringify({
                "tweet_text": tweet_text,
                "segment_id": segment_id,
                "program_id": program_id,
                "last_menu_url": window_url,
                "address_array" : addressArray,
        });
        console.log(dataSet);

        $.ajax({url: "/verify_twitter",
            type: "POST",
            data: dataSet,
            contentType: 'json;charset=UTF-8',
            cache: false,
            success: function(data) {

                // Success message
                console.log('success');
                if(data['redirectURL']){
                     window.location.href = data['redirectURL'];
                } else {
                    var len = data['successArray'].length;
                    console.log(data['successArray'].length);
                    console.log(data['duplicateArray'].length);
                    if(data['successArray'].length !=0){
                        successArray = data['successArray'];
                    } else {
                        successArray = [];
                    }

                    if(data['duplicateArray'].length !=0){
                        duplicateArray = data['duplicateArray'];
                    } else {
                        duplicateArray = [];
                    }

                    function hideLoading(){
                        $('.loader').hide();
                        $('.tweet-loader').hide();
                    }

                    if (successArray.length > 0){
                        $.when(hideLoading()).then(showSuccess(successArray, duplicateArray)).then($('#close-button').trigger('click'));
                        //showSuccess(successArray, duplicateArray);
                    } else {
                        $.when(hideLoading()).then(showSuccess(successArray, duplicateArray));
                    }
                }
            },
            error: function() {
                $('.loader').hide();
                // Fail message
                console.log('fail :)');
            }
        });
      }
    });


    $('#text-input').keyup(function() {
        var placeholderLength = $('.address-placeholder').text().length
        value = $('#text-input').html();
        searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
        if (searchBool == -1){
//            console.log("span is NOT there, adding");
            $('#text-input').html('<span contenteditable=false class=address-placeholder></span>' + value);
            $('.action-panel-container').each(function(){
                 if ($(this).hasClass( "selected" )){
                    $(this).removeClass('selected');
                 }
            });
            $('.address-item').each(function(){
                $(this).removeClass('selected');
            });




        }

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems
        $('#send-button-label').text(labelText);
    });
});






// show duplicate method
function showDuplicate(duplicateArray){
    if (duplicateArray.length != 0){
        duplicateArray.forEach(function (value, i) {
            console.log('%d: %s', i, value);
            var tweetName = value.slice(1)
            var idText = '#success-box-' + tweetName;
            $(idText).each(function(){
                $(this).css({'opacity':'0.0'});
                $(this).css({'background':'#800000'});
                $(this).animate({'height':'0.0'},0,function() {
                    $(this).css({'width':'10px'});
                });
                $(this).animate({'height':'58.0'},300,function() {
                    $(this).css({'opacity':'1.0'});
                    $(this).show();
                    $(this).animate({'width':'200px'},600,function() {
                        $(this).contents('.duplicate-text').css({'opacity':'1.0'});
                        $(this).contents('.duplicate-text').show();
                        $(this).animate({'width':'200px'},1500,function() {
                            $(this).contents('.duplicate-text').css({'opacity':'0.0'});
                            $(this).contents('.duplicate-text').css({'display':'none'});
                            $(this).animate({'width':'10px'},600,function() {
                                $(this).animate({'height':'0px'},300,function(){
                                    $(this).css({'opacity':'0.0'});
                                    $(this).css({'display':'none'});
                                });
                            });
                        });
                    });
                });
            });
        });
    } else {
        console.log('no dpulicates');
    }
}


function showSuccess(successArray, duplicateArray){
    if (successArray.length != 0){
        successArray.forEach(function (value, i) {
            var tweetName = value.slice(1)
            var idText = '#success-box-' + tweetName;
            var idSuccessIndicator = '#success-indicator-' + tweetName;
            $(idText).each(function(){
                $(this).css({'opacity':'0.0'});
                $(this).css({'background':'green'});
                $(this).animate({'height':'0.0'},0,function() {
                    $(this).css({'width':'10px'});
                });
                $(this).animate({'height':'58.0'},300,function() {
                    $(this).css({'opacity':'1.0'});
                    $(this).show();
                    $(this).animate({'width':'200px'},600,function() {
                        $(this).contents('.success-text').css({'opacity':'1.0'});
                        $(this).contents('.success-text').show();
                        $(this).animate({'width':'200px'},1500,function() {
                            $(this).contents('.success-text').css({'opacity':'0.0'});
                            $(this).contents('.success-text').css({'display':'none'});
                            $(this).animate({'width':'10px'},600,function() {
                                $(this).animate({'height':'0px'},300,function(){
                                    $(this).css({'display':'none'});
                                    $(this).animate({'opacity':'0.0'},0,function(){
                                        $(idSuccessIndicator).show();
                                        showDuplicate(duplicateArray);
                                    });
                                });
                            });
                        });
                    });
                });
            });
        });
    } else {
        showDuplicate(duplicateArray);
        console.log('no success, going to duplicateArray')
    }
}




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

            //            console.log(data)
            //            data.forEach(function (dict, i) {
            //                field = dict['value']
            //                    if(field == 'NAME_FIRST'){
            //                        console.log('yes, first name');
            //                    } else {
            //                        console.log('not, first name');
            //                    }
            //                    console.log(dict['value']);
            //
            //
            //
            //            });

//            console.log("Congress fields:"+ data[0][bioguideId]);
            //var congressDataArray = data['congressData'];
            //console.log(congressDataArray)
            //var len = congressDataArray.length;
            //form_boom(data);
        },
        error: function() {
            console.log('failure in get email fields content_landing.js');
        }
    });
}

function form_boom(data){
    requiredActions = data["F000062"]["required_actions"];
    requiredActions.forEach(function (fieldItem, i) {
        console.log(fieldItem["value"]);

    });
}

    function get_congress(zip){
        $.ajax({url: "/get_congress/" + zip,
            type: "GET",
            data: "",
            contentType: 'json;charset=UTF-8',
            cache: false,
            success: function(data) {
//                console.log(data);
                // hide loading indicator
                $('#zip-loader').hide();

                // Count if any results returned, if not, go back
                var index = 0;
                var i;
                var s;
                var congressDataArray = data['congressData'];
//                console.log(congressDataArray)
                var len = congressDataArray.length;
                if(len == 0){
                    alert("We aren't able to find representatives for that zip code.  Please check your zip code and try again.");
                    $('.zip-input').focus();
                    $('.submit-zip').show();
                    return false;
                }
                // hide zip cature, clear zip input
                $('.zip-capture').hide();
                $('.zip-input').val('');

                // show zip indicator, to allow reset
                $('.zip-indicator').show();

                for (i=0; i<len; ++i) {
                  if (i in congressDataArray) {
                    var item = congressDataArray[i];

                    // Image check
                    var imageString;
                    if(!item['image']['url']){
                       imageString = '<img class="repPhoto repPhoto-none" src=\'/static/img/push-thought-logo.png\'>';
                    } else {
                       imageString = '<img class="repPhoto" id="repPhoto'+i+'" src="'+item['image']['url']+'">';
                    }

                    // twitterId check
                    var twitterIdString;
                    if(!item['twitter_id']){
                       twitterIdString = ['<div class="twitter-name" id="twitter-name-'+i+'">n/a</div>',
                        '<img class="twitter-icon-empty" src=\'/static/img/twitter-icon-gray.png\' width="42" height="42">',
                        '<div class="warning-box-tweet-icon">',
                            '<p class="warning-text">twitter address n/a</p>',
                        '</div>'
                        ].join("\n");
                    } else {
                       twitterIdString = ['<div class="twitter-name" id="twitter-name-'+i+'">@'+item['twitter_id']+'</div>',
                            '<img class="twitter-icon" src=\'/static/img/twitter-icon.png\' width="42" height="42">'
                            ].join("\n");
                    }

                    // contact form check
                    var emailString;
                    if(!item['contact_form']){
                       emailString =  ['<div class="email-name" id="'+i+'" name="'+ item['full_name'] + '">n/a</div>',
                       '<img class="email-icon-gray" id="email-icon-'+i+'name="'+item['full_name']+'" src=\'/static/img/email-icon-gray.png\' width="36" height="36">',
                       '<div hidden class="bioguide-mule" id="'+item['bioguide_id']+'"></div>'].join("\n");
                    } else {
                       emailString =  ['<div class="email-name" id="'+i+'" name="'+ item['full_name'] + '">see below</div>',
                       '<img class="email-icon" id="email-icon-'+i+'" name="'+item['full_name']+'" src=\'/static/img/email-icon.png\' width="36" height="36">',
                       '<div hidden class="bioguide-mule" id="'+item['bioguide_id']+'"></div>'].join("\n");
                    }

                    // sent user count
                    var sentCountDiv
                    if(!item['sent_messages_count']){
                        sentCountDiv  = '';
                    } else {
                        sentCountDiv = '<div class="sent-messages-count">' +item['sent_messages_count']+'</div>';
                    }


                    // user touched check
                    var indicatorString;
                    if(!item['userTouched']){
                       indicatorString = '<img style="display:none" class="success-indicator" id="success-indicator-'+ item['twitter_id'] +'" src=\'/static/img/check-green.png\'>';
                    } else {
                        indicatorString = '<img class="success-indicator" id="success-indicator-'+ item['twitter_id'] +'" src=\'/static/img/check-green.png\'>';
                    }


                    // construct HTML for contacts in category
                    var text =  [
                        '<div class="rep-item-container rep-item-container-' + i +'">',
                            '<div class="rep-item" id="rep-item'+i+'">',
                              '<div class="loader loader-'+i+ '" id="loader"></div>',
                                sentCountDiv,
                               indicatorString,
                              '<p hidden id="tweet-address-item'+i+'">@'+item['twitter_id']+'</p>',
                              '<div class="success-box" id="success-box-'+item['twitter_id']+'">',
                                      '<p class="success-text" style="padding-top:4px;">tweet sent to:</p>',
                                      '<p class="success-text" style="font-size:14pt; color:#00aced;">@'+item['twitter_id']+'</p>',
                                      '<p class="duplicate-text" style="padding-top:4px;">duplicate, not sent:</p>',
                                      '<p class="duplicate-text" style="font-size:14pt; color:#00aced;">@'+item['twitter_id']+'</p>',
                              '</div>',
                              '<div style="display:inline-block;">',
                               imageString,
                                    '<div class="name-title-container">',
                                         '<div><p class="full-name">'+ item['full_name']+'</p></div>',
                                         '<div><p class="title">'+item['title']+'</p></div>',
                                    '</div>',
                              '</div>',
                            '</div>',
                            '<div class="action-panel-container" id="'+i+'">',
                                    '<div class="action-panel">',
                                        twitterIdString,
                                        '<img class="phone-icon" id="'+item['phone']+'" name="'+item['full_name']+'" src=\'/static/img/phone-icon.png\'>',
                                        emailString,
                                    '</div>',
                            '</div>',
                        '</div>'
                    ].join("\n");
                    $('.rep-container').append(text);

                    //                    // HTML option for twitter address addressLabel above input box
                    //                    if(item['twitter_id']){
                    //                        var addressText;
                    //                        addressText = [
                    //                          '<div class="address-item address-item-'+i+'">',
                    //                             '<p class="address-label-'+i+'">@'+item['twitter_id']+'</p>',
                    //                          '</div>'
                    //                        ].join("\n");
                    //                        $('.address-container').append(addressText);
                    //                    }
                  }
                }
            },
            error: function() {
                $('#zip-loader').hide();
                console.log('failure pulling congress data - in content_landing.js');
            }
        });
    }