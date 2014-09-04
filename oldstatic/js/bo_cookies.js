$(document).on('click', "#upd-coordinates", function() {
        var coord = $('#txt-coordinates').val().split(',');
        $.cookie('MyLat', coord[0], { path: '/'});
        $.cookie('MyLon', coord[1], { path: '/'});
	});