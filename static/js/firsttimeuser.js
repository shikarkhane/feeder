$(function() {
            if ($.cookie('FirstTimeUser')){
                window.location.replace("/we/feed/");
            };
        });

$(document).on('click', "#gotit", function() {
    $.cookie('FirstTimeUser', 1, { expires: 30, path: '/'});
    window.location.replace("/");
});