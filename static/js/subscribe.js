


$(document).on('click', "#btnsubscribe", function(event) {
    event.preventDefault();
    var email = $('#txtsubscribe').val().replace(/\s+/g, '');
    var lat = $.cookie('MyLat'), lon = $.cookie('MyLon');
    var location_url_part = '';
    if (lat){
        location_url_part = location_url_part + 'location/' + lat + '/' + lon + '/';
    }

    if ((email.length == 0) || !(isValidEmail(email))){
        $('#inSubscribeEmail').val('Not valid!');
        console.log('Subscribe email not valid');
    }
    else{
        var jqxhr = $.post( get_servername_from_url() + 'subscribe/'+ email +'/' + location_url_part );
        $.cookie('subscribed',  true, { expires: 700, path: '/'});
        $('#txtsubscribe').val('Subscribed!');
    }
});