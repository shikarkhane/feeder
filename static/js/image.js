
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
}

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
}
