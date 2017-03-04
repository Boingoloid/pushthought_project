




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
        $('.submit-zip').trigger('click');
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
        console.log(data[1][0]);


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

            //if ($(this).attr('id').length < 5 ){
        //    alert('sorry, no email form yet for this person.');
        //} else {
        //    var contactPath = $(this).attr('id');
        //    window.open(contactPath);
        //}
        //window.open('mailto:test@example.com?subject=subject&body=body');

        // stop if animation in progress
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }

        var bioguideId = $(this).attr('name');
        get_congress_email_fields(bioguideId);  //get fields from db or phantom congress

        // show action container
        $('.rep-action-container').css('display','block'),200,function(){
        };

        // scroll to appropriate place on screen to see action container
        $('.category-container').animate({'height':'350px'},200,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });

        // hide items that disappear
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});
        $('.twitter-icon').animate({'opacity':'0'});
        $('.twitter-icon').css('display','none')
        $('.twitter-icon-empty').animate({'opacity':'0'});
        $('.twitter-icon-empty').css('display','none')
        $('.phone-icon').animate({'opacity':'0'});
        $('.phone-icon').css('display','none')
        $('.email-icon').animate({'opacity':'0'});
        $('.email-icon').css('display','none')
        $('.email-icon-gray').animate({'opacity':'0'});
        $('.email-icon-gray').css('display','none')

        // show twitter name
        $('.email-name').show();
        $('.email-name').animate({'opacity':'1.0'},400,function(){
        });

        // toggle selection for activity container with clicked email icon
        $(this).parent('div').parent('div').toggleClass("selected");

        // toggle address paths above text input
        var index = $(this).parent('div').parent('div').attr('id');
        var addressPath = ".email-address-item-" + index;
        $(addressPath).toggleClass('selected');

        // show Send button
        $('#img-send-tweet-icon').hide();
        $('#img-send-email-icon').show();

        // write text in Send label for number selected
        var numItems = $('.address-item.selected').length;
        var labelText = 'email: ' + numItems;
        $('#tweet-button-label').text(labelText);
        $('#text-input').focus();


    });

    $('.rep-container').on("click", "img.twitter-icon", function() {
        var i = $(this).attr('id');
        console.log("i:" + i);

        // if animation occuring, stop method
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
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

        // hide items that disappear
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'});
        $('.twitter-icon').css('display','none');
        $('.twitter-icon-empty').css('display','none');
        $('.phone-icon').css('display','none');
        $('.email-icon').css('display','none');
        $('.email-icon-gray').css('display','none');

        // show twitter name
        $('.twitter-name').show();

        // toggle selection of activity container
//        $(this).parent('div').parent('div').toggleClass("selected");
        $('.action-panel-contianer#'+i).toggleClass("selected");

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
        var addressPath = String(".address-node-" + i)
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
        $('#button-label').text(labelText);

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
        $('.address-container').html(' ');
        $('.category-container').animate({'height':'220px'});
        $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
            $('.rep-action-container').css('display','none');
        })
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


    });


    $('.rep-container').on("click", ".action-panel-container", function() {
        var i = $(this).attr('id');
        var text = $('#twitter-name-'+i).text();
        console.log(text);

        if(!$('.twitter-name').is(":visible")) {
            return false;
        } else if(  text == 'n/a'){
            alert('Don\'t have a twitter account for this rep yet.  We\'re working on it.  Thank you for your patience.');
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

            // update placeholderText and button label -> based on # of addresses selected
            var numItems = $('.address-item.selected').length;
            var labelText = 'tweet: ' + numItems
            $('#button-label').text(labelText);
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
                    // remove twitter name above textarea
                    var index = $(this).attr('id');
                    var addressPath = ".address-item-" + index;
                    $(addressPath).removeClass('selected');
                 }
            });
        }

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems
        $('#tweet-button-label').text(labelText);
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

            console.log(data)
            data.forEach(function (dict, i) {
                field = dict['value']
                    if(field == 'NAME_FIRST'){
                        console.log('yes, first name');
                    } else {
                        console.log('not, first name');
                    }
                    console.log(dict['value']);



            });

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
                console.log(data);
                // hide loading indicator
                $('#zip-loader').hide();

                // Count if any results returned, if not, go back
                var index = 0;
                var i;
                var s;
                var congressDataArray = data['congressData'];
                console.log(congressDataArray)
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
                console.log(len);

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
                       twitterIdString = ['<div class="twitter-name" id="twitter-name">n/a</div>',
                        '<img class="twitter-icon-empty" src=\'/static/img/twitter-icon-gray.png\' width="42" height="42">',
                        '<div class="warning-box-tweet-icon">',
                            '<p class="warning-text">twitter address n/a</p>',
                        '</div>'
                        ].join("\n");
                    } else {
                       twitterIdString = ['<div class="twitter-name">@'+item['twitter_id']+'</div>',
                            '<div hidden class="index">'+i+'</div>',
                            '<img class="twitter-icon" src=\'/static/img/twitter-icon.png\' width="42" height="42">'
                            ].join("\n");
                    }

                    // contact form check
                    var emailString;
                    if(!item['contact_form']){
                       emailString = '<img class="email-icon-gray" id="'+item['contact_form']+'name="'+item['bioguide_id']+'" src=\'/static/img/email-icon-gray.png\' width="36" height="36">';
                    } else {
                       emailString = '<img class="email-icon" id="'+item['contact_form']+'name="'+item['bioguide_id']+'" src=\'/static/img/email-icon.png\' width="36" height="36">';
                    }

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

                    // HTML option for twitter address addressLabel above input box
                    if(item['twitter_id']){
                        var addressText;
                        addressText = [
                          '<div class="address-item address-item-'+i+'">',
                             '<p class="address-label-'+i+'">@'+item['twitter_id']+'</p>',
                          '</div>'
                        ].join("\n");
                        $('.address-container').append(addressText);
                    }
                  }
                }
            },
            error: function() {
                $('#zip-loader').hide();
                console.log('failure pulling congress data - in content_landing.js');
            }
        });
    }