function set_active_channel(channel) {
    $('.rep-container').prop('class', function(i, c) {
        return c.replace(/(^|\s)active-channel-\S+/g, '') +
            ' active-channel-' + channel;
    });
}


function set_active_mode(mode) {
    $('.rep-container').prop('class', function(i, c) {
        return c.replace(/(^|\s)active-mode-\S+/g, '') + ' active-mode-' + mode;
    });
}


function set_status(element, status_name) {
    status_text = {
        'success': "Success!",
        'unknown_congressman': "Unknown congressman",
        'too_long': "Too many characters",
        'duplicate': "Duplicate Tweet",
        'error': "Error",
    }
    $(element)
        .prop('class', function(i, c) {
            return c.replace(/(^|\s)active-mode-\S+/g, '') + ' ' + status_name;
        })
        .text(status_text[status_name] || "Status unknown");
}


function show_congressmen_status(statuses) {
    $('.twitter-name').each(function() {
        status_panel = $(this).parent().siblings('.status-panel');
        twitter_handle = $(this).text().slice(1);
        if (twitter_handle in statuses) {
            set_status(status_panel, statuses[twitter_handle]);
        }
    });
    $('.email-name').each(function() {
        status_panel = $(this).parent().siblings('.status-panel');
        bioguide = $(this).data('bioguide');
        if (bioguide in statuses) {
            set_status(status_panel, statuses[bioguide]);
        }
    });
}


function show_status(data) {
    focus_on_text_input();
    if (data.status == 'no_mentions') {
        alert("No recipients found.");
    } else {
        show_congressmen_status(data.statuses);
        if (['success'].includes(data.status)) {
            close_form();
        }
        set_active_mode('status');

        $('.status-panel, .action-panel-container .action-panel').each(
            function() {
                full_height = $(this).css('height');
                $(this).css('height', 0).animate({'height': full_height}, 500);
            });
    }
    $('#tweet-button').prop('disabled', true);
}


function hide_status() {
    function change_active_mode() {
        if ($('.rep-action-container').not('.hiding').is(":visible")) {
            set_active_mode('selection');
            $('.status-panel.success')
                .parents('.action-panel-container.selected')
                .click();
            focus_on_text_input();
        } else {
            set_active_mode('action');
        }
    }

    if ($('.rep-container').hasClass('active-mode-status')) {
        $('.status-panel, .action-panel-container .action-panel').each(
            function() {
                full_height = $(this).css('height');
                $(this).animate({'height': 0}, 500, complete=function() {
                    $(this).css('height', full_height);
                    change_active_mode();
                });
            });
    } else {
        change_active_mode();
    }
    $('#tweet-button').prop('disabled', false);
}
