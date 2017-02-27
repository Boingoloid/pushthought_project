


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");

$(document).ready(function() {



    function get_congress(){
        var zip = $('.zip-input').val();
        zip = '94107';
        $.ajax({url: "/get_congress/" + zip,
            type: "GET",
            data: "",
            contentType: 'json;charset=UTF-8',
            cache: false,
            success: function(data) {
                console.log(data);
                // put in congress data
                // for each insert through js the html
                var index = 0;

                var i, s, myStringArray = data['congressData'], len = myStringArray.length;
                for (i=0; i<len; ++i) {
                  if (i in myStringArray) {
                    var item = myStringArray[i];

                    // Image check
                    var imageString
                    if(!item['image']['url']){
                       imageString = '<img class="repPhoto repPhoto-none" src=\'/static/img/push-thought-logo.png\'>';
                    } else {
                       imageString = '<img class="repPhoto" id="repPhoto'+i+'" src="'+item['image']['url']+'">';
                    }

                    // twitterId check
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
                    if(!item['contact_form']){
                       emailString = '<img class="email-icon" id="'+item['contact_form']+'" src=\'/static/img/email-icon-gray.png\' width="36" height="36">';
                    } else {
                       emailString = '<img class="email-icon" id="'+item['contact_form']+'" src=\'/static/img/email-icon.png\' width="36" height="36">';
                    }


                    // construct HTML
                    var text =  [
                        '<div class="rep-item-container rep-item-container-' + i +'">',
                            '<div class="rep-item" id="rep-item'+i+'">',
                              '<div class="loader loader-'+i+ '" id="loader"></div>',
                              '<img style="" class="success-indicator" id="success-indicator-'+ item['twitter_id'] +'" src=\'/static/img/check-green.png\'>',
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
//                    $('.drop-here').append(text);

                    //s = myStringArray[i]['twitter_id'];
                    //console.log("here is the item:" + s);
                  }
                }

//                            {% endif %}

//                            {% if item.contact_form %}
//                                <img class="email-icon" id="{{ item.contact_form }}" src="{% static 'img/email-icon.png' %}" width="36" height="36">
//                            {% else %}
//                                <img class="email-icon" id="{{ item.contact_form }}" src="{% static 'img/email-icon-gray.png' %}" width="36" height="36">
//                            {% endif %}
//                        </div>
//                    </div>
//                </div>
//                }




//                            <!--<img class="img-logo-success" src="{% static 'img/push_thought_logo3.png' %}" width="70" height="70">-->

















                },
            error: function() {
                console.log('fail');
            }
        });
    }
    get_congress();


    $('.zip-input').click( function() {
        $('.submit-zip').show();
    });

    $(document).mouseup(function(){
        if ($('.zip-input') == "focused"){

        } else{
            if($(".submit-zip:visible").length==1){
                $(".submit-zip").hide(); // Toggle
            }
        }
    });

   $('.submit-zip').click( function() {
        // validators
        var zip = $('.zip-input').val();
        var isValidZip = /(^\d{5}$)/.test(zip);

        if (isValidZip){
            console.log('valid zip');
        } else{
            console.log('NOT a valid zip');
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


    var csrftoken = Cookies.get('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });



    $('.watch-button').click( function() {
       //var idText = $(this).attr('id');
       //var repIndex = idText.replace('program-item','');
       //var programObjectIdElementName = "#program-item-objectId" + repIndex;
       //var programObjectId = $(programObjectIdElementName).text();
       window.location.href="/leaving";
    });

    $('.rep-container').on("click", "img.twitter-icon", function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        };

        $('.rep-action-container').css('display','block'),200,function(){
            //var caretPos = $("#text-input").selectionStart;
            //var textAreaTxt = $("#text-input").val();
            //var txtToAdd = "stuff";
            //$("#text-input").val(textAreaTxt.substring(0, caretPos) + txtToAdd + textAreaTxt.substring(caretPos));
        };
        $('.category-container').animate({'height':'350px'},200,function(){
            var headerAllowance = $('.seen-it-container').offset().top - 20;
            $('html, body').animate({
                scrollTop: headerAllowance + 'px'
            }, 'fast');
        });
        $('.rep-color-band').animate({'height':'375px'});
        $('.rep-action-container').animate({'opacity':'1.0','height':'135px'},500,function() {
            });
        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').animate({'opacity':'0'});
        $('.twitter-icon').css('display','none')
        $('.twitter-icon-empty').animate({'opacity':'0'});
        $('.twitter-icon-empty').css('display','none')
        $('.phone-icon').animate({'opacity':'0'});
        $('.phone-icon').css('display','none')
        $('.email-icon').animate({'opacity':'0'});
        $('.email-icon').css('display','none')
        $('.twitter-name').animate({'opacity':'1.0'},400,function(){
        });
        $(this).parent('div').parent('div').toggleClass("selected");

        var index = $(this).parent('div').parent('div').attr('id');
        //console.log(index);
        var addressPath = ".address-item-" + index;
        //console.log(addressPath);
        $(addressPath).toggleClass('selected');

        addressPlaceholderClass= '.address-label-' + index;
        addressPlaceholder = $(addressPlaceholderClass).html()
        stringSpace = '&nbsp';
        $('#text-input').html('<span contenteditable=false class=address-placeholder>' + addressPlaceholder + '</span>');

        //var tweetText = $('#text-input').text();
        //letterCount = tweetText.length;
        //console.log("letter count:" + letterCount);

        // set button label
        var numItems = $('.address-item.selected').length;
        var labelText = 'tweet: ' + numItems
        $('#tweet-button-label').text(labelText);


        $('#text-input').focus();
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
    //alert("twitter clicked");

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

    $('.rep-container').on("click", "img.email-icon", function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }

        text = $(this).attr('id');
        console.log(text);

        if ($(this).attr('id').length < 5 ){
            alert('sorry, no email form yet for this person.');
        } else {
            var contactPath = $(this).attr('id');
            window.open(contactPath);
        }

        //window.open('mailto:test@example.com?subject=subject&body=body');
    });

    $('#close-button').on('click',function(event) {
        //if ($(':animated').length) {
        //    console.log("cancelling close button click");
        //    return false;
        //}
        $('.category-container').animate({'height':'220px'});
        $('.rep-action-container').animate({'opacity':'0.0','height':'0px'},500,function() {
            $('.rep-action-container').css('display','none')
        })
        //$('.twitter-icon').animate({'left':'42%'});
        $('.twitter-icon').animate({'opacity':'1'});
        $('.twitter-icon').show()
        $('.twitter-icon-empty').animate({'opacity':'1'});
        $('.twitter-icon-empty').show();
        $('.phone-icon').animate({'opacity':'1'});
        $('.phone-icon').show();
        $('.email-icon').animate({'opacity':'1'});
        $('.email-icon').show();
        $('.twitter-name').animate({'opacity':'0.0'});
        $('.rep-color-band').animate({'height':'233px'});
        $('.selected').animate($('.selected').removeClass('selected'));
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


    $('.action-panel-container').on('click', function(){
        if($('.twitter-name').css('opacity') == 0) {
            return false
        } else {
            if ($(this).hasClass( "selected" )){
                $(this).removeClass('selected');
                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-item-" + index;
                $(addressPath).removeClass('selected');
            } else {
                $(this).addClass('selected');
                // add or remove twitter name above textarea
                var index = $(this).attr('id');
                var addressPath = ".address-item-" + index;
                $(addressPath).addClass('selected');
            }

            var placeholderLength = $('.address-placeholder').text().length
            value = $('#text-input').html();
            searchBool = value.search("<span contenteditable=\"false\" class=\"address-placeholder\">");
            if (searchBool == -1){
                $('#text-input').html(value + '<span contenteditable=false class=address-placeholder></span>');
            }

            var numItems = $('.address-item.selected').length;
            var labelText = 'tweet: ' + numItems
            $('#tweet-button-label').text(labelText);
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

   $('#tweet-button').on('click',function(event) {

      var tweet_text = $('#text-input').text();
      if(tweet_text.length < 1){
        alert ("Please type a message to tweet first");
      } else {

        addressArray = [];
        $('.action-panel-container.selected').each(function() {
            index = $(this).attr('id');
            function showLoading(index){
                var loaderDiv = '.loader-' + index;
                console.log(loaderDiv);
                $(loaderDiv).show();
            }
            showLoading(index);

            twitterName = $(this).contents().contents('.twitter-name').text();
            addressArray.push(twitterName);
         });
        alert(tweet_text);
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

//html('<span contenteditable=false class=address-placeholder>''</span>');


//    function insertTextAtCursor(text) {
//        var sel, range, html;
//        if (window.getSelection) {
//            sel = window.getSelection();
//            if (sel.getRangeAt && sel.rangeCount) {
//                range = sel.getRangeAt(0);
//                range.deleteContents();
//                range.insertNode( document.createNode(text));
//            }
//        } else if (document.selection && document.selection.createRange) {
//            document.selection.createRange().text = text;
//        }
//    }

//    function updatePlaceholder(){
//        var numItems = $('.address-item.selected').length;
//        console.log(numItems);
//    }


//    // CLICK ACTIONS
//    $('.rep-container').on('click','.rep-item',function(event) {
//        // extract index # of click and grab twitter address
//       var idText = $(this).attr('id');
//       var repIndex = idText.replace('rep-item','');
//       var tweetAddressID = "#tweet-address-item" + repIndex;
//       var tweetAddress = $(tweetAddressID).text();
//       var currentText = $('#text-input').val();
//
//
//       if ($(this).css('background-color') === 'rgb(255, 255, 255)'){
//
//         $(this).css('background-color','green');
//         currentText += tweetAddress;
//         $('#text-input').val(currentText);
//
//       } else {
//
//        $(this).css('background-color','white');
//        var n = currentText.search(tweetAddress);
//        //console.log(n);
//        var re = new RegExp(tweetAddress,"gi");
//        var newText = currentText.replace(re,"");
//        $('#text-input').val(newText);
//       }
//    });

//    $('.tweet-container').on('click','.tweet-item',function(event) {
//       var idText = $(this).attr('id');
//       var tweetIndex = idText.replace('tweet-item','');
//
//       var tweetObjectIdElementName = "#tweet-item-objectId" + tweetIndex;
//       var tweetObjectId = $(programObjectIdElementName).text();
//       window.location.href="/content_landing/" + tweetObjectId;
//    });

//        window.location.href = window_url;

//        Create and encode URL
//        var encodedTweetText = encodeURIComponent(tweetText);

//	function insertAtCaret(areaId, text) {
//		var txtarea = $('#text-input');
//		if (!txtarea) { return; }
//
//		var scrollPos = txtarea.scrollTop;
//		var strPos = 0;
//		var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
//			"ff" : (document.selection ? "ie" : false ) );
//		if (br == "ie") {
//			txtarea.focus();
//			var range = document.selection.createRange();
//			range.moveStart ('character', -txtarea.html.length);
//			strPos = range.text.length;
//		} else if (br == "ff") {
//			strPos = txtarea.selectionStart;
//		}
//
//		var front = (txtarea.html).substring(0, strPos);
//		var back = (txtarea.html).substring(strPos, txtarea.html.length);
//		txtarea.html = front + text + back;
//		strPos = strPos + text.length;
//		if (br == "ie") {
//			txtarea.focus();
//			var ieRange = document.selection.createRange();
//			ieRange.moveStart ('character', -txtarea.html.length);
//			ieRange.moveStart ('character', strPos);
//			ieRange.moveEnd ('character', 0);
//			ieRange.select();
//		} else if (br == "ff") {
//			txtarea.selectionStart = strPos;
//			txtarea.selectionEnd = strPos;
//			txtarea.focus();
//		}
//
//		txtarea.scrollTop = scrollPos;
//	}

//    insertAtCaret('#text-input', 'text to insert')