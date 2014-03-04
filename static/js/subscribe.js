

$( "#form-subscribe" ).submit(function( event ) {
    event.preventDefault();
    var email = $('#inSubscribeEmail').val().replace(/\s+/g, '');

    if ((email.length == 0) || !(isValidEmail(email))){
        $('#div-subscribe').removeClass('alert-info').addClass('alert-danger');
    }
    else{
        var jqxhr = $.post( $.cookie('myservername') + 'subscribe/'+ email +'/');
        $.cookie('subscribed',  true, { expires: 700, path: '/'});
        $('#inSubscribeEmail').val('');
        $('#div-subscribe').addClass('hide');
    }
});