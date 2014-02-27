$(function() {
        $('#home-brand > span').attr('class', 'glyphicon glyphicon-chevron-left');

        var timelabel = moment(formatDate(new Date($('#time_since').text())), "YYYY-MM-DDTHH:mm:ssZ").fromNow();
        $('#time_since').html(timelabel);

        var mainpost_id = $("div.main-post");
        var coordinates = $(mainpost_id).find("div.coord").text();
        insert_map(mainpost_id, coordinates);
        google.maps.event.addDomListener(window, 'resize', insert_map);
        google.maps.event.addDomListener(window, 'load', insert_map);
});

$(document).on('click', "#home-brand", function(event){
        parent.history.back();
        return false;
});

$( "#popular-frame" ).error(function() {
        $('#pop-div').remove();
});