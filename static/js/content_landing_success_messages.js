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
    var status2text = {
        null: "",
        'success': "Success!",
        'too_long': "Too many characters",
        'duplicate': "Duplicate Tweet",
        'unknown_error': "Error",
    }
    var status_text = status2text.hasOwnProperty(status_name) ?
        status2text[status_name] : status_name;
    element
        .prop('class', function(i, c) {
            var classes = [c.replace(/(^|\s)status_\S+/g, '')];
            if (status_name !== null) {
                if (status_name != 'success') {
                    classes.push('status_error');
                }
                classes.push('status_' + status_name);
            }
            return classes.join(' ');
        })
        .text(status_text);
}


function show_congressmen_status(statuses, type) {
    var handle2status_panel = {}
    $('.' + type + '-name').each(function() {
        if (type == 'twitter') {
            var handle = $(this).text().slice(1);
        } else if (type == 'email') {
            var handle = $(this).data('bioguide');
        }
        handle2status_panel[handle] = $(this).parent().siblings(
            '.status-panel');
    });
    Object.keys(handle2status_panel).forEach(function(handle) {
        set_status(handle2status_panel[handle], statuses[handle] || null);
        // Select congressman to whom message wasn't sent successfully or
        // deselect ones to whom was sent successfully (they can be previously
        // deselected if sending went through Twitter auth) or who weren't among
        // receivers.
        if (handle2status_panel[handle].parent().hasClass('selected') ==
                (!statuses.hasOwnProperty(handle) ||
                    statuses[handle] == 'success')) {
            handle2status_panel[handle].siblings('.selection-panel').click();
        }
    });
}


function show_statuses(data, type, sent_via_ajax=true) {
    if (data.status == 'no_mentions') {
        alert("No recipients found.");
        return;
    }
    if (data.status == 'success') {
        close_form();
    } else {
        if (!sent_via_ajax && type == 'twitter' &&
                $('.rep-action-container').is(":hidden")) {
            // Show tweeting form if there are errors and sending went through
            // Twitter auth.
            $('.twitter-icon').click();
        }
    }
    show_congressmen_status(data.statuses, type);
    set_active_mode('status');

    $('.status-panel, .action-panel-container .action-panel').each(
        function() {
            var full_height = $(this).css('height');
            $(this).css('height', 0).animate({'height': full_height}, 500);
        });
    $('#tweet-button').prop('disabled', true);
}


function hide_status() {
    function change_active_mode() {
        if ($('.rep-action-container').not('.hiding').is(":visible")) {
            set_active_mode('selection');
            focus_on_text_input();
        } else {
            set_active_mode('action');
        }
    }

    if ($('.rep-container').hasClass('active-mode-status')) {
        $('.status-panel, .action-panel-container .action-panel').each(
            function() {
                var full_height = $(this).css('height');
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
