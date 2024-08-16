$(document).ready(function() {
    $('.tabs div').click(function() {
        var tabId = $(this).attr('id').replace('-tab', '-content');

        $('.tabs div').removeClass('active');
        $(this).addClass('active');

        $('.tab-content').removeClass('active-tab');
        $('#' + tabId).addClass('active-tab');
    });

    // Initially show the first tab content
    $('.tabs div').first().click();
});
