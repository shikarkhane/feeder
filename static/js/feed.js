function getFeedUrl(){
            var from_datetime = new Date().getTime();
            var q_pagesize = 20;
            var mylat = $.cookie('MyLat');
            var mylon = $.cookie('MyLon');
            var fromposition = $.cookie('FromPosition');
            var mysearchradius = $.cookie('mysearchradius');
            var mysortbyvotes = $.cookie('mysortbyvotes');
			var myfilterdays = $.cookie('myfilterdays');

            if (!myfilterdays){ myfilterdays = 100; }
            if (!fromposition){ fromposition = 0; }
            if (!mysearchradius){ mysearchradius = 9; }
            if (!mysortbyvotes){ mysortbyvotes = 0; }

            var servername = get_servername_from_url();
            //servername = 'http://tipoff.io/';

			var path = servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize
			            + "/radius/" + mysearchradius + '/sort/' + mysortbyvotes + '/filterdays/' + myfilterdays + '/';
			var popular_path = path;

	  		if (!($.cookie('MyLat') == null)){			  				
	    			path = path +  "location/" + mylat + "/" +  mylon + "/";
	    			popular_path = popular_path +  "location/" + mylat + "/" +  mylon + "/";
	    		}
	    	popular_path = popular_path + "source/instagram/";
			// getAndRenderData(path, popular_path);
			handlePageNumber(1, q_pagesize);
			return path;
};


function handlePageNumber(code, q_pagesize){
	if (code == 1){ 
			setFromPosition();
			var nextposition = parseInt($.cookie('FromPosition')) + q_pagesize;
			$.cookie('FromPosition', nextposition, { path: '/'});
	};
	if (code == -1){ //decrement by step size
			setFromPosition();
			var nextposition = parseInt($.cookie('FromPosition')) - q_pagesize;
			if (nextposition < 0){
				nextposition = 0;
			}
			$.cookie('FromPosition', nextposition, { path: '/'}); 
	};
};
function setFromPosition(){
		if (($.cookie('FromPosition') == null)||($.cookie('FromPosition') == "NaN")){
			$.cookie('FromPosition', 0, { path: '/'});
		};
	};

//LOAD FEED FIRST
loadFeed();
// MASORY FEED

$container = $(".feed ");

$container.masonry({
  itemSelector        : '.item',
  columnWidth         : '.item',
  transitionDuration  : 0
});




// INFINITE SCROLLING

function element_in_scroll(elem)
{
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}


$(window).scroll(function(e){
    if (element_in_scroll(".loadingmore")) {
        $(document).unbind('scroll');
        loadFeed();
    }

});


// LOAD FEED
function loadFeed(){
    var url = getFeedUrl();
    $.get(url,function(res)
    {
        data = JSON.parse(res);
        for(var i = 0; i < data.length; i++)
        {
            //social: insta, fb =facebook, tw = twitter, gplus = google plus
            $container.append('<div id="'+data[i].doc_id+'" class="item col-xs-12 col-sm-6 col-md-4 col-lg-3"><div class="itemcontent"><div class="photo lazyload" data-original="'+data[i].content_img_url+'"></div><div class="profilePhoto lazyload" data-original="'+data[i].user_img_url+'"></div><div class="boxpadding"><div class="'+data[i].social+'-icon"></div><a href="#"><div class="more">...</div></a><p class="postcontent">'+data[i].text+'</p><div class="bottom"><h5 class="timeago primary"  title="'+formatDate(new Date(data[i].created))+'"></h5><div class="like">'+data[i].up_votes+'</div><div class="distance" data-coord="'+data[i].coord+'">1km</div></div></div></div></div></div>').masonry('reloadItems').masonry('layout');
        }
        $(".feed .lazyload:not(.loaded)").lazyload({
            effect : "fadeIn"
        }).addClass("loaded");
        $(".timeago:not(.timeloaded)").timeago().addClass("timeloaded");

        //LIKE TOGGLE

        $(".like:not(.activated)").click(function()
        {
            var count = parseInt($(this).html());
            var increment = 1;
            var doc_id = $(this).closest("div.item").attr("id");
            if($(this).hasClass("liked"))
            {
                $(this).html(count-1);
                increment = -1;
            }
            else
            {
                $(this).html(count+1);
            }
            $(this).toggleClass("liked");
            var jqxhr = $.get( get_servername_from_url() + 'like/'+ encodeURIComponent(doc_id) +'/' + increment + '/');

        }).addClass("activated");

        //LOAD MAP

        $(".distance").colorbox({
            maxWidth: "80%",
            maxHeight: "80%",
            html:'<div id="gmap_canvas" style="width:750px; height:500px;"></div>',
            scrolling:false,
            onComplete:function()
            {
                init_map($(this).attr('data-coord'));
            }
        });
        function init_map(coordinates)
        {
            var coord = coordinates.split(',');
            var myOptions =
            {
                zoom:14,
                center:new google.maps.LatLng(coord[0],coord[1]),
                mapTypeId: google.maps.MapTypeId.ROADMAP

            };
            map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);
            marker = new google.maps.Marker(
            {
                map: map,
                position: new google.maps.LatLng(coord[0], coord[1])

            });


        }


    });

    // redirect to nofeed
    checkIfMainFeedEmpty();
};

