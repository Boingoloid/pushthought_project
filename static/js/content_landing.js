


function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function show_success_message() {
    $('.success-box').css({'opacity':'1'});
    $('.success-box').animate({'opacity':'0.0'},2500,function() {});
}

$(document).ready(function() {

    if ($('#successArray').val()){
      alert($('#successArray').val());
      for (item in successArray) {
        $('.success-indicator-' + str(item)).each(function() {
            $(this).css({'opacity':'1'});
            $(this).animate({'opacity':'0.0'},2500,function() {});
        });
      }
    } else {
        alert('no value');
        alert($('#successArray').val());
    }

//    setTimeout(function() {
//        $(".twitter-icon").trigger('click');
//    },10);

    var csrftoken = Cookies.get('csrftoken');
    //var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();  //this also works
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
        alert("phone clicked");
    });

    $('.email-icon').click( function() {
        if ($(':animated').length || $(this).css('opacity') == 0) {
            return false;
        }
        alert("email clicked");
    });

    $('#close-button').on('click',function(event) {
        if ($(':animated').length) {
            console.log("cancelling close button click");
            return false;
        }
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

    $('#tweet-button').on('click',function(event) {

      var tweet_text = $('#text-input').text();

      if(tweet_text.length < 1){
        alert ("Please type a message to tweet first");
      } else {
        var successArray = [];
        $('.action-panel-container.selected').each(function() {
            twitterName = $(this).contents().contents('.twitter-name').text();
            successArray.push(twitterName);
            console.log(twitterName);
        });

        dataSet = JSON.stringify({
                "tweet_text": tweet_text,
                "segment_id": segment_id,
                "program_id": program_id,
                "last_menu_url": window_url,
                "successArray" : successArray
        });
         $.ajax({url: "/verify_twitter",
                type: "POST",
                data: dataSet,
                contentType: 'json;charset=UTF-8',
                cache: false,
                success: function(data) {
                    // Success message
                    console.log('success');
                    window.location.href = data['redirectURL'];
                },
                error: function() {
                    // Fail message
                    console.log('fail :)');
                }
         });
      }
    });
//    var textStart = '';
//    var textEnd = '';
//    var placeholderText = '';


    $('#text-input').keydown(function() {
        var inputText = $('#text-input').text();
        textStart = $(this).html();
        console.log(textStart);
        var numItems = $('.address-item.selected').length;


//        placeholderTextSpace = placeholderText;
    });

    $('#text-input').keyup(function() {

//        var re = /@/.test(inputText);
//        var remulti = /@multiple/.test(inputText);
//        console.log(remulti);

            // add back placeholder if it was deleted
        if (!$(this).contents().hasClass('address-placeholder')){
//                insertTextAtCursor('<span contenteditable=false class=address-placeholder></span>');
//                $('.address-item.selected').each(function() {
//                    $('address-item').removeClass('selected');
//                });
            $(this).html(textStart);
        }

        console.log($(this).hasClass('address-placeholder'));
        console.log($(this).html());
//        console.log('output');
//        console.log('textStart:' + textStart);
//        console.log('textEnd:' + textEnd);
//        console.log("placeholder" + placeholderText);

//        if (textEnd.indexOf(placeholderText) > -1){
//            console.log("index of placeholder" + textEnd.indexOf(placeholderText));
//            return false;
//        } else if ($('.placeholderText').text() == '') {
//            console.log('blank placeholderText')
//            return false;
//        } else {
////            console.log("index of placeholder" + textEnd.indexOf(placeholderText));
//            alert("This is where will put the twitter names.  Add text before and after.");
//            $(this).html(textStart);
//            textStart = '';
//            textEnd = '';
//            placeholderText = '';
//        }
    });


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


//html('<span contenteditable=false class=address-placeholder>''</span>');


    function insertTextAtCursor(text) {
        var sel, range, html;
        if (window.getSelection) {
            sel = window.getSelection();
            if (sel.getRangeAt && sel.rangeCount) {
                range = sel.getRangeAt(0);
                range.deleteContents();
                range.insertNode( document.createNode(text));
            }
        } else if (document.selection && document.selection.createRange) {
            document.selection.createRange().text = text;
        }
    }

    function updatePlaceholder(){
        var numItems = $('.address-item.selected').length;
        console.log(numItems);
    }


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

	function insertAtCaret(areaId, text) {
		var txtarea = $('#text-input');
		if (!txtarea) { return; }

		var scrollPos = txtarea.scrollTop;
		var strPos = 0;
		var br = ((txtarea.selectionStart || txtarea.selectionStart == '0') ?
			"ff" : (document.selection ? "ie" : false ) );
		if (br == "ie") {
			txtarea.focus();
			var range = document.selection.createRange();
			range.moveStart ('character', -txtarea.html.length);
			strPos = range.text.length;
		} else if (br == "ff") {
			strPos = txtarea.selectionStart;
		}

		var front = (txtarea.html).substring(0, strPos);
		var back = (txtarea.html).substring(strPos, txtarea.html.length);
		txtarea.html = front + text + back;
		strPos = strPos + text.length;
		if (br == "ie") {
			txtarea.focus();
			var ieRange = document.selection.createRange();
			ieRange.moveStart ('character', -txtarea.html.length);
			ieRange.moveStart ('character', strPos);
			ieRange.moveEnd ('character', 0);
			ieRange.select();
		} else if (br == "ff") {
			txtarea.selectionStart = strPos;
			txtarea.selectionEnd = strPos;
			txtarea.focus();
		}

		txtarea.scrollTop = scrollPos;
	}

//    insertAtCaret('#text-input', 'text to insert')


});