





// show duplicate method
function showDuplicate(duplicateArray){
    // if (duplicateArray.length != 0){
    if (duplicateArray){
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
        console.log('no duplicates in alert array');
    }
}


function showSuccess(successArray, duplicateArray){
    // if (successArray.length != 0){
    if (successArray){
        successArray.forEach(function (value, i) {
            var tweetName = value.slice(1) //chop off @ at start
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
        console.log('no success messages in alert array, going to duplicate array')
        showDuplicate(duplicateArray);

    }
}

function showEmailSuccess(bioguideArray){
    if (bioguideArray.length != 0){
        bioguideArray.forEach(function (value, i) {
            var bioguide = value
            var successBoxId = '#success-box-' + bioguide;
            var fullName = $(successBoxId).attr('name');

            alertHTML = [
            '<p class="alert-text" style="padding-top:4px;">email sent to:</p>',
            '<p class="success-text" style="padding-top:4px;">'+fullName+'</p>'
            ].join("\n");
            $(successBoxId).append(alertHTML);
        });

        bioguideArray.forEach(function (value, i) {
            var bioguide = value
            var successBoxId = '#success-box-' + bioguide;
            var fullName = $(successBoxId).attr('name');
            var idSuccessIndicator = '#success-indicator-' + bioguide;

            $(successBoxId).css({'width':'0px', 'height':'0px'});
            $(successBoxId).show();
            $(successBoxId).animate({'width':'10.0'},0,function() {
            });
            $(successBoxId).animate({'height':'58.0'},300,function() {
                $(successBoxId).animate({'width':'200px'},600,function() {
                    $(successBoxId).contents('.success-text').show();
                    setTimeout(function(){
                        $(successBoxId).contents('.success-text').hide();
                        $(successBoxId).animate({'width':'10px'},600,function() {
                            $(successBoxId).animate({'height':'0px'},300,function(){
                                $(successBoxId).css({'width':'0px'});
                                $(successBoxId).hide();
                                $(idSuccessIndicator).show();
                                $(successBoxId).html('');
                            });
                        });
                    }, 1500); // how long message shows
                });
            });
        });
    } else {
        console.log('no email success array');
    }
}