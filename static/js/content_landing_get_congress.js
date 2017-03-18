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

            for (x=0; x<len; ++x) {
              //console.log('i in the loop:'+i);  // this loop starts at 0
              if (x in congressDataArray) {
                var item = congressDataArray[x];

                var i = x + 1; //needs to match {{ forloop.counter }} of other html templated objects
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
//                if(!item['contact_form']){
//                   emailString =  ['<div class="email-name email-name-'+ item['bioguide_id'] +'" id="'+i+'" name="'+ item['full_name'] + '">click to toggle</div>',
//                   '<img class="email-icon-gray" id="email-icon-'+i+'name="'+item['full_name']+'" src=\'/static/img/email-icon-gray.png\' width="36" height="36">',
//                   '<div hidden class="bioguide-mule" id="'+item['bioguide_id']+'">'+item['last_name']+'</div>'].join("\n");
//                } else {
                   emailString =  ['<div class="email-name email-name-'+ item['bioguide_id'] +'" id="'+i+'" name="'+ item['full_name'] + '">see below</div>',
                   '<img class="email-icon" id="email-icon-'+i+'" name="'+item['full_name']+'" src=\'/static/img/email-icon.png\' width="36" height="36">',
                   '<div hidden class="bioguide-mule" id="'+item['bioguide_id']+'">'+item['last_name']+'</div>'].join("\n");
//                }

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
              }
            }
        },
        error: function() {
            $('#zip-loader').hide();
            console.log('failure pulling congress data - in content_landing.js');
        }
    });
}

function form_boom(data){
    requiredActions = data["F000062"]["required_actions"];
    requiredActions.forEach(function (fieldItem, i) {
        console.log(fieldItem["value"]);

    });
}
