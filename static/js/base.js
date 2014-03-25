
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

$(document).on('click', "a.post-like", function() {
        $('#in-progress-wheel').removeClass('hide');
		var doc_id = $(this).closest("div.main-post").attr("id");
		var likecount = parseInt($(this).text(), 10);
        var increment;
        if($(this).hasClass('btn-info')){
                increment = -1;
                $(this).removeClass('btn-info');
            }
        else{
               increment = 1;
               $(this).addClass('btn-info');
        }
        likecount = likecount + increment;
		var jqxhr = $.get( $.cookie('myservername') + 'like/'+ encodeURIComponent(doc_id) +'/' + increment + '/');
		$(this).html('<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp;' + likecount);
        $('#in-progress-wheel').addClass('hide');
	});
$(document).on('click', "#delete-post", function() {
        var doc_id = $(this).closest("div.main-post").attr("id");
		var jqxhr = $.get( $.cookie('myservername') + 'delete/'+ encodeURIComponent(doc_id) +'/' );
		window.location.replace("/");
	});

