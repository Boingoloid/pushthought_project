function showTwitterStatus(successArray, duplicateArray, errorArray){
    if (successArray && successArray.length) {
        alert('Success: ' + successArray.join(", "));
    }
    if (duplicateArray && duplicateArray.length) {
        alert('Dublicates: ' + duplicateArray.join(", "));
    }
    if (errorArray && errorArray.length) {
        alert('Errors: ' + errorArray.join(", "));
    }
}

function showEmailSuccess(bioguideArray){
    if (bioguideArray.length) {
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
