


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}






//}function show_success_message() {
//    if ($('#successArray').val()){
//      alert($('#successArray').val());
//      console.log($('#successArray').val());
//      for (item in successArray) {
//            var refText = '.success-box-' + str(item)
//            $(refText).each(function() {
//                $('.success-box').each(function() {
//                    $('.success-text').css({'opacity':'0.0'});
//                    $(this).animate({'height':'0.0'},0,function() {
//                        $(this).css({'width':'10px'});
//                        $(this).css({'opacity':'1.0'});
//                        $(this).show();
//                    });
//                    $(this).animate({'height':'58.0'},300,function() {
//                        $(this).animate({'width':'200px'},600,function() {
//                            $('.success-text').css({'opacity':'1.0'});
//                            $(this).animate({'width':'200px'},1500,function() {
//                                $('.success-text').css({'opacity':'0.0'});
//                                $(this).animate({'width':'10px'},600,function() {
//                                    $(this).animate({'height':'0px'},300,function(){});
//                                });
//                            });
//                        });
//                    });
//                });
//            });
//      }
//    } else {
//    }
//}

//testWindow = window.open("popup.php","interaction","resizable=0,width=800,height=600,status=0");

$(document).ready(function() {


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

    $('.twitter-icon').click(function() {
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
                $("#text-input").val("@multiple")
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

        var tweetText = $('#text-input').text();
        letterCount = tweetText.length;
        console.log("letter count:" + letterCount);

        $('#text-input').focus();
        range = window.getSelection().getRangeAt(0);
        range.setStart(range.endContainer,range.endOffset);
        //document.execCommand('selectAll',false,null);
        console.log(window.getSelection().getRangeAt(0));
        var selection = window.getSelection();

        $('#text-input').val('');
        //selection.focusOffset = 3;
        //selection.focus(3);
        //console.log("selection.focusNode.data[selection.focusOffset]" + selection.focusNode.data[selection.focusOffset]);
        //        alert(selection.focusOffset);
        //var index = tweetText.indexOf()
        //document.selection.select
    });


    //<span>' + stringSpace + '</span>
    $('.twitter-icon-empty').click(function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            console.log("cancelling twitter empty icon click, animation or item invisible");
            return false;
        }

        $('.warning-box-tweet-icon').css({'opacity':'1'});
        $('.warning-box-tweet-icon').animate({'opacity':'0.0'},2500,function() {});
    });
    //alert("twitter clicked");

    $('.phone-icon').click( function() {
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

    $('.email-icon').click( function() {
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
            //console.log(window.getSelection().getRangeAt(0));
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

            // add back placeholder if it was deleted
            //            if (!$('text-input').hasClass('address-placeholder')){
            //                $('text-input').focus();
            //                $('text-input').select();
            //                insertTextAtCursor('<span contenteditable=false class=address-placeholder></span>');
               //            }
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
        var addressArray = [];

        // make addressArray:  array of twitter names to attempt
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


        // create dataSet string
        dataSet = JSON.stringify({
                "tweet_text": tweet_text,
                "segment_id": segment_id,
                "program_id": program_id,
                "last_menu_url": window_url,
                "addressArray" : addressArray,
        });

        console.log(dataSet);

        // Grab success array
//        var successArray = JSON.parse(dataSet)['addressArray'];
//        var duplicateArray = JSON.parse(dataSet)['addressArray'];
//        console.log(successArray);
//        console.log('DUPLICATE:')
//        console.log(duplicateArray);
//        var lengthValue = duplicateArray.length;
//        console.log(lengthValue);
        //showSuccess(successArray, duplicateArray);
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
            //    $('#text-input').keydown(function() {
            //        var inputText = $('#text-input').text();
            //        textStart = $(this).html();
            //        console.log(textStart);
            //        var numItems = $('.address-item.selected').length;
            //    });



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