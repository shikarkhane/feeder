function pad(num) {
    return ("0" + num).slice(-2);
};

function formatDate(d) {
    return [d.getUTCFullYear(), 
            pad(d.getUTCMonth() + 1), 
            pad(d.getUTCDate())].join("-") + "T" + 
           [pad(d.getUTCHours()), 
            pad(d.getUTCMinutes()), 
            pad(d.getUTCSeconds())].join(":") + "Z";
};
function getDate30MinFromNow(){
     var date = new Date();
     var minutes = 30;
     date.setTime(date.getTime() + (minutes * 60 * 1000));
     return date;
 };

 // Convert dataURL to Blob object
function dataURLtoBlob(dataURL) {
    // Decode the dataURL
    var binary = atob(dataURL.split(',')[1]);
    // Create 8-bit unsigned array
    var array = [];

    for(var i = 0; i < binary.length; i++) {
      array.push(binary.charCodeAt(i));
    }
    // Return our Blob object
    return new Blob([new Uint8Array(array)], {type: 'image/png'});
};

function get_url_value(param){
    if(param=(new RegExp('[?&]'+encodeURIComponent(param)+'=([^&]*)')).exec(location.search))
        return decodeURIComponent(param[1]);
};

function insert_map(append_to_object, coordinates) {
    var coord = coordinates.split(',');
   var mapOptions = {
           zoom: 14,
           center: new google.maps.LatLng(coord[0],coord[1])
       };
    var divmap = document.createElement('div');
    divmap.setAttribute("id", "mapCanvas");
    divmap.setAttribute("class", "mapCanvas");
    append_to_object.append(divmap);

   var map = new google.maps.Map(divmap, mapOptions);

   var marker = new google.maps.Marker({
                   map: map,
                   draggable: false,
                   position: new google.maps.LatLng(coord[0],coord[1])
       });
};

function reverseLookupLocality(lat, lng) {
    geocoder = new google.maps.Geocoder();
  var localityname= 'Pluto!';
  var latlng = new google.maps.LatLng(lat, lng);
  var stage;
  geocoder.geocode({'latLng': latlng}, function(result, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      if (result[1]) {
            console.log(result);
            $.each( result, function( i, item ) {
                console.log(item);
                if (jQuery.inArray( 'sublocality', item['types'] ) > -1){
                    stage = item['address_components'];
                    return false;
                }
             });
             $.each( stage, function( i, item ) {
                    console.log(item);
                    if (jQuery.inArray( 'sublocality', item['types'] ) > -1){
                        localityname = item['short_name'];
                        $.cookie('mylocalityname', localityname, { path: '/'});
                        setLocalityName();
                        return false;
                    }
             });
      } else {
        localityname = 'Aliens';
      }
    } else {
      console.log('Geocoder failed due to: ' + status);
    }
  });
  return localityname;
};

function setLocalityName(){
    var name = 'Pluto!'
    console.log($.cookie('mylocalityname'));
    if ($.cookie('mylocalityname')){
        name = $.cookie('mylocalityname');
    }
    $('#home-brand > span').html( name);
};

$(function() {
    setLocalityName();
});

function getIpAddress(){
    url = 'http://jsonip.com/';
    $.getJSON( url, function( data ) {
        return data['ip'];
    });
};

function setLocationBasedOnIpaddress(){
    var url = 'http://ipinfo.io/json';
    var cityname;
    $.getJSON( url, function( data ) {
        cityname = data['city'];
        if (!(cityname)){
            cityname = 'Pluto!';
        }
        $.cookie('mylocalityname', cityname, { path: '/'});
        setLocalityName();
    });
};

function setCoordinatesByLocation(locality){
    var lat;
    var lon;



    $.cookie('MyLat', lat, { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
    $.cookie('MyLon', lon, { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
};

function peekFromBottomOfScreen(object){
     var viewportWidth = jQuery(window).width(),
            viewportHeight = jQuery(window).height(),
            $foo = object,
            elWidth = $foo.width(),
            elHeight = $foo.height(),
            elOffset = $foo.offset();

        jQuery(window)
            .scrollTop(elOffset.top - (viewportHeight/2));

}
