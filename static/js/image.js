
// For reusing canvas instance of detectVerticalSquash
var canvas;

/**
 * 'Fixes' single canvas instances.
 * Leaving the canvas html detection.
 */
function fixCanvas(canvas)
{
    var ctx = canvas.getContext('2d');
    var drawImage = ctx.drawImage;
    ctx.drawImage = function(img, sx, sy, sw, sh, dx, dy, dw, dh)
    {
        var vertSquashRatio = 1;
        // Detect if img param is indeed image
        if (!!img && img.nodeName == 'IMG')
        {
            vertSquashRatio = detectVerticalSquash(img);
            sw || (sw = img.naturalWidth);
            sh || (sh = img.naturalHeight);
        }

        // Execute several cases (Firefox does not handle undefined as no param)
        // by call (apply is bad performance)
        if (arguments.length == 9)
            drawImage.call(ctx, img, sx, sy, sw, sh, dx, dy, dw, dh / vertSquashRatio);
        else if (typeof sw != 'undefined')
            drawImage.call(ctx, img, sx, sy, sw, sh / vertSquashRatio);
        else
            drawImage.call(ctx, img, sx, sy);
    };
    return canvas;
};

/**
 * Detecting vertical squash in loaded image.
 * Fixes a bug which squash image vertically while drawing into canvas for some images.
 * This is a bug in iOS6 devices. This function from https://github.com/stomita/ios-imagefile-megapixel
 *
 */
function detectVerticalSquash(img) {
    var ih = img.naturalHeight;
    canvas = canvas || document.createElement('canvas');
    canvas.width = 1;
    canvas.height = ih;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    try {
        // Prevent cross origin error
        var data = ctx.getImageData(0, 0, 1, ih).data;
    } catch (err) {
        // hopeless, assume the image is well and good.
        console.log("Cannot check verticalSquash: CORS?");
        return 1;
    }
    // search image edge pixel position in case it is squashed vertically.
    var sy = 0;
    var ey = ih;
    var py = ih;
    while (py > sy) {
        var alpha = data[(py - 1) * 4 + 3];
        if (alpha === 0) {
            ey = py;
        } else {
            sy = py;
        }
        py = (ey + sy) >> 1;
    }
    var ratio = (py / ih);
    return (ratio===0)?1:ratio;
};

var image_on_canvas = 0;

$(function() {
		var imageLoader = document.getElementById('imageLoader');
		imageLoader.addEventListener('change', handleImage, false);

		function handleImage(e){
            $('#in-progress-wheel').removeClass('hide');

		    var reader = new FileReader();
		    reader.onload = function(event){

                var canvasEl = fixCanvas(document.createElement('canvas'));
                canvasEl.setAttribute("id", "imageCanvas");
                $('#divcanvas').append(canvasEl);

                var imgEl = document.createElement('img');
                imgEl.onload = function()
                {
                    var ctx = canvasEl.getContext('2d');
                    ctx.drawImage(this, 0, 0, 243, 243);
        		    window.image_on_canvas = 1;
                    $('#imageLoader').remove();
                    $('#btn-upload').removeAttr('disabled');
                    $('#btn-upload').addClass('btn-success').removeClass('btn-default');
                    $('#in-progress-wheel').addClass('hide');

                };
                imgEl.src = event.target.result;
		    }
		    reader.readAsDataURL(e.target.files[0]);
		}
});

$(document).on('click', "#btn-upload", function() {

		var text = encodeURIComponent($('#tagline').val());
		if (text.length == 0){alert('Comments are missing!'); return;}
		if (window.image_on_canvas == 0){alert('Image is missing!'); return;}

		var lat = $.cookie('MyLat');
		var lon = $.cookie('MyLon');
        var cityname = $.cookie('mylocalityname');

		if (lat){
            $('#in-progress-wheel').removeClass('hide');
			var imgfile= dataURLtoBlob(document.getElementById('imageCanvas').toDataURL());
			var fd = new FormData();
			fd.append("image", imgfile);

			$.ajax({
				  type: "POST",
				  url: "/new/location/" + lat + "/" + lon + "/text/"  + text + "/place/" + cityname + "/",
				  data: fd,
				  processData: false,
   				  contentType: false,
				}).done(function( respond ) {
                            $('#in-progress-wheel').addClass('hide');
						})
                     .fail(function(respond) {
                            //alert(respond);
                            //alert( "Something went wrong!" );
                            $('#in-progress-wheel').addClass('hide');
                    });
            alert('Your tipoff is being uploaded!\nIt will appear shortly in the listing.');
            window.location.replace("/");
		}
	});
