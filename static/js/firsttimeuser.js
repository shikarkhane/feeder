$(document).on('click', "#gotit", function() {
    $.cookie('FirstTimeUser', 1, { expires: 30, path: '/'});
    window.location.replace("/");
});