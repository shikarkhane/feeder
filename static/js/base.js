
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
   //console.log(coordinates);
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

function base_get_servername_from_url(){
    var url = window.location.pathname;
    var servername = 'http://' + $('<a>').prop('href', url).prop('hostname');
	if (!($('<a>').prop('href', url).prop('port') == null)){
		servername = 'http://' + $('<a>').prop('href', url).prop('hostname') + ':' + $('<a>').prop('href', url).prop('port');
	}
	return servername;
};

$(document).on('click', "a.share-buttons-class", function() {
        event.preventDefault();
        var pathname = base_get_servername_from_url() + window.location.pathname;
        var href = "http://www.facebook.com/sharer.php?u=" + pathname;
        //console.log(this.id);
        if ( this.id == 'fbshare'){
            href = "http://www.facebook.com/sharer.php?u=" + pathname;
        }
        else if ( this.id == 'twittershare'){
            href = "http://twitter.com/share?url=" + pathname + "&text=Neighbourhood vibes";
        }
        else if ( this.id == 'gplusshare'){
            href = "https://plus.google.com/share?url=" + pathname;
        }
        else if ( this.id == 'diggshare'){
            href = "http://www.digg.com/submit?url=" + pathname;
        }
        else if ( this.id == 'redditshare'){
            href = "http://reddit.com/submit?url=" + pathname;
        }
        else if ( this.id == 'linkedinshare'){
            href = "http://www.linkedin.com/shareArticle?mini=true&url=" + pathname;
        }
        else if ( this.id == 'stumbleuponfbshare'){
            href = "http://www.stumbleupon.com/submit?url=" + pathname + "&title=Neighbourhood vibes";
        }
        else {
            href = "mailto:?Subject=Neighbourhood vibes&Body=I%20saw%20this%20and%20thought%20of%20you!%20 " + pathname;
        }
        console.log(href);
        window.open(href);
	});

