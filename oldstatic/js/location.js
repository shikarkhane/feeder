
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
    $('#home-brand > span').html( name);
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
    $.getJSON( url, function( data ) {
        //console.log('calling ip info');
        coord = data['loc'];
        //console.log(coord);
        if (coord){
                //console.log(coord);
                $.cookie('MyLat', coord.split(',')[0], { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
                $.cookie('MyLon', coord.split(',')[1], { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
                //console.log('before call');
                getFeedData(window.pageload_utctime, window.default_pagesize*3, $.cookie('MyLat'), $.cookie('MyLon'),
			$.cookie('FromPosition'), $.cookie('myFilterTags'), $.cookie('mysearchradius'), $.cookie('mysortbyvotes'));
			    //console.log('after call');
                reverseLookupLocality(coord.split(',')[0], coord.split(',')[1]);
        }
    });
};