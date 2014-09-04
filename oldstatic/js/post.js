$(function() {


        var timelabel = moment(formatDate(new Date($('#time_since').text())), "YYYY-MM-DDTHH:mm:ssZ").fromNow();
        $('#time_since').html(timelabel);

        var mainpost_id = $("div.main-post");
        var coordinates = $(mainpost_id).find("div.coord").text();
        //console.log(coordinates);
        insert_map(mainpost_id, coordinates);
        //google.maps.event.addDomListener(window, 'resize', insert_map);
        //google.maps.event.addDomListener(window, 'load', insert_map);
});



$( "#popular-frame" ).error(function() {
        $('#pop-div').remove();
});

$(document).on('click', "a.choose-category", function(event){
    event.preventDefault();
    $('#selected-category').html(this.text);
    $.post( this.href, function( data ) {
            console.log(data);
    });
});
