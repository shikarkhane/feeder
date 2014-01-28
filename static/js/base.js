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
}

