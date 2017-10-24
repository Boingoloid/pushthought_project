$(document).ready(function () {
    $(document).on('change', '#twitter_input_add_url', function () {
        if ($(this).prop('checked')) {
            var url = ' pushthought.com/' + window.location.href.split('/').slice(3).join('/');
            var url_span = '<span id="text-input-url" contenteditable=false class="address-placeholder"> ' + url + '</span>'
            var text = $('#text-input').html();
            $('#text-input').html(text + url_span);
        } else {
            $('#text-input-url').remove();
        }
    })
});
    function get_longest_address(){
            var longestAddressLength = 0;
            $('.address-item-label:visible').each(function(){
                var text = $(this).text();
                if (text.length > longestAddressLength){
                    longestAddressLength = text.length;
                }
            });
            return longestAddressLength;
    }
    function updateTextCount(){
        var textInput = $('#text-input').text();
        var twitterMax = 140;
        var twitterDefaultLinkLength = 22;
        var countAfterLink = twitterMax - twitterDefaultLinkLength;

        var addressInput = $('.address-placeholder').text();
        var countAddressInput =  addressInput.length;
        var countTextInput =  textInput.length;
        var longestAddressLength = get_longest_address();
        var countRemaining = countAfterLink - countTextInput + countAddressInput - longestAddressLength;


        // adjust for line breaks
        numberOfLineBreaks = (textInput.match(/\n/g)||[]).length;
        countRemaining = countRemaining - numberOfLineBreaks;

        $('.letter-count').text(countRemaining);
        if (countRemaining < 0){
            $('.letter-count').css({'color':'red'});
        } else {
            $('.letter-count').css({'color':'gray'});
        }
    }