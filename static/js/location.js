
function reverseLookupLocality(lat, lng) {
//alert(lat + ',' + lng);
  var  geocoder = new google.maps.Geocoder();
  var localityname= '';
  var latlng = new google.maps.LatLng(lat, lng);
  var stage;
  //alert(geocoder);
  geocoder.geocode({'latLng': latlng}, function(result, status) {
  //alert(status);
    if (status == google.maps.GeocoderStatus.OK) {

      if (result[1]) {
            //console.log(result);
            $.each( result, function( i, item ) {
                //console.log(item);
                if ((jQuery.inArray( 'sublocality', item['types'] ) > -1) || (jQuery.inArray( 'locality', item['types'] ) > -1)){
                    stage = item['address_components'];
                    return false;
                }
             });
             $.each( stage, function( i, item ) {
                    //console.log(item);
                    if ((jQuery.inArray( 'sublocality', item['types'] ) > -1) || (jQuery.inArray( 'locality', item['types'] ) > -1)){
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
      //console.log('Geocoder failed due to: ' + status);
    }
  });
  return localityname;
};

function setLocalityName(){
    var name = ''
    //console.log($.cookie('mylocalityname'));
    if ($.cookie('mylocalityname')){
        name = $.cookie('mylocalityname');
    }
    $('#localityName').html( name);
};

function getIpAddress(){
    url = 'http://jsonip.com/';
    $.getJSON( url, function( data ) {
        return data['ip'];
    });
};

function setLocationBasedOnIpaddress(){
    //console.log('set location by ip');
    var url = 'http://ipinfo.io/json';
    $.ajax({
        dataType: "json",
        url: url,
        async: false
        })
        .done(function( data ) {
            // console.log('calling ip info');
            coord = data['loc'];
            // console.log(coord);
            if (coord){
                    // console.log(coord);
                    $.cookie('MyLat', coord.split(',')[0], { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
                    $.cookie('MyLon', coord.split(',')[1], { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
                    $.cookie('FromPosition', 0, { path: '/'});
                    reverseLookupLocality(coord.split(',')[0], coord.split(',')[1]);
            }
        });

    $.getJSON( url, function( data ) {
        //console.log('calling ip info');
        coord = data['loc'];
        //console.log(coord);
        if (coord){
                console.log(coord);
                $.cookie('MyLat', coord.split(',')[0], { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
                $.cookie('MyLon', coord.split(',')[1], { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
                $.cookie('FromPosition', 0, { path: '/'});
                reverseLookupLocality(coord.split(',')[0], coord.split(',')[1]);
        }
    });
};

function couldntFetchPositionByGps(msg){
        setGpsOffText();
		$.cookie('gpsAllowedByUser', 0, { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
};

function setCoordinateCookie(position){
            //alert('set coord');
		  	$.cookie('MyLat', position.coords.latitude, { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
			$.cookie('MyLon', position.coords.longitude, { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
			$.cookie('FromPosition', 0, { path: '/'});
            $.cookie('LocationByGps', 1, { expires:getDate30MinFromNow(), path: '/'}); // flag that location is by ip addr
            reverseLookupLocality($.cookie('MyLat'), $.cookie('MyLon'));
		 };

function setLocationUsingGPS(){
console.log('before navigate');
        if (navigator.geolocation){
            $('#in-progress-wheel').removeClass('hide');
            navigator.geolocation.getCurrentPosition(setCoordinateCookie, couldntFetchPositionByGps, {timeout:5000});
        };
}


function setGpsOnText(){
            $("div.gps").addClass("active");
            $(".gps h6").html("GPS ON");
            $("h6.location-by-text").html("(using your gps)");
};

function setGpsOffText(){
            $("div.gps").removeClass("active");
            $(".gps h6").html("ENABLE GPS");
            $("h6.location-by-text").html("(using your IP Address)");
};


