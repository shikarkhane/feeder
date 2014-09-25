$(function() {
            if ($.cookie('FirstTimeUser')){
                window.location.replace("/we/feed/");
            };
        });

$(document).on('click', "#a-first-time-user", function() {
    $.cookie('FirstTimeUser', 1, { expires: 30, path: '/'});
    window.location.replace("/we/feed/");
});