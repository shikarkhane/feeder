function getFeedUrl(){
            var from_datetime = new Date().getTime();
            var q_pagesize = 20;
            var mylat = $.cookie('MyLat');
            var mylon = $.cookie('MyLon');
            var fromposition = $.cookie('FromPosition');
            var mysearchradius = $.cookie('mysearchradius');
            var mysortbyvotes = $.cookie('mysortbyvotes');
			var myfilterdays = $.cookie('myfilterdays');

            if ($.cookie('from_datetime')){
                from_datetime = $.cookie('from_datetime');
            }
            if (!myfilterdays){
                myfilterdays = 30;
                $.cookie('myfilterdays', myfilterdays, { path: '/'});
                $(".variable2").ionRangeSlider("update", { from: myfilterdays });
                }
            if (!fromposition){
                fromposition = 0;
                $.cookie('FromPosition', fromposition, { path: '/'});
                }
            if (!mysearchradius){
                mysearchradius = 9;
                $.cookie('mysearchradius', mysearchradius, { path: '/'});
                $(".variable3").ionRangeSlider("update", { from: mysearchradius });
                }
            if (!mysortbyvotes){
                mysortbyvotes = 0;
                $.cookie('mysortbyvotes', mysortbyvotes, { path: '/'});
                }

            var servername = get_servername_from_url();
            //servername = 'http://tipoff.io/';

			var path = servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize
			            + "/radius/" + mysearchradius + '/sort/' + mysortbyvotes + '/filterdays/' + myfilterdays + '/';
			var popular_path = path;

            if ($.cookie('MyLat')){
                    path = path +  "location/" + mylat + "/" +  mylon + "/";
            }
            else{
            //hard code stockholm for time being ( 59.324801, 18.072453 )
            // TODO: implement require and add dependency so that location loads first
                    path = path +  "location/59.324801/18.072453/";
            }

			return path;
};


function handlePageNumber(q_pagesize){
        setFromPosition();
        var nextposition = parseInt($.cookie('FromPosition')) + q_pagesize;
        $.cookie('FromPosition', nextposition, { path: '/'});
        console.log('inside handlepagenumber');
        console.log(nextposition);
        console.log(parseInt($.cookie('FromPosition')));
};
function setFromPosition(){
		if (($.cookie('FromPosition') == null)||($.cookie('FromPosition') == "NaN")){
			$.cookie('FromPosition', 0, { path: '/'});
		};
	};


$(document).ready(function()
{
    console.log('feed loaded');
    $.cookie('from_datetime', new Date().getTime(), { path: '/'});

    //LOAD FEED FIRST
    loadFeed();
    // MASORY FEED

    $container = $(".feed ");

    $container.masonry({
      itemSelector        : '.item',
      columnWidth         : '.item',
      transitionDuration  : 0
    });
});

function changeLoadingMoreMessage(msg){
    $('.loadingmore').html(msg);
}

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

//LIKE TOGGLE
$(document).on('click', ".like:not(.activated)", function()
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

// LOAD FEED
function loadFeed(){
    var url = getFeedUrl();
    console.log(url);
    $.get(url,function(res)
    {
        handlePageNumber(20);
        data = JSON.parse(res);
        if ( data.length == 0 ){
            changeLoadingMoreMessage('End of feed!');
        }

        for(var i = 0; i < data.length; i++)
        {
            //social: insta, fb =facebook, tw = twitter, gplus = google plus
            $container.append('<div id="'+data[i].doc_id+'" class="item col-xs-12 col-sm-6 col-md-4 col-lg-3"><div class="itemcontent"><div class="photo lazyload" data-original="'+data[i].content_img_url+'"></div><div class="profilePhoto lazyload" data-original="'+data[i].user_img_url+'"></div><div class="boxpadding"><div class="'+data[i].source+'-icon"></div><a href="'+data[i].user_profile_url+'" target="_blank"><div class="more">...</div></a><p class="postcontent post-text">'+data[i].text+'</p><div class="bottom"><h5 class="timeago primary"  title="'+formatDate(new Date(data[i].created))+'"></h5><div class="like">'+data[i].up_votes+'</div><div class="distance" data-coord="'+data[i].coord+'">'+Math.round(data[i].distance)+'km</div></div></div></div></div></div>').masonry('reloadItems').masonry('layout');
        }

        $(".feed .lazyload:not(.loaded)").lazyload({
            effect : "fadeIn"
        }).addClass("loaded");
        $(".timeago:not(.timeloaded)").timeago().addClass("timeloaded");



        //LOAD MAP

        $(".distance").colorbox({
            maxWidth: "80%",
            maxHeight: "80%",
            html:'<div id="gmap_canvas" style="width:'+ ($(window).width() * 0.80) + 'px; height:'+ ($(window).height() * 0.80) + 'px;"></div>',
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
                center:new google.maps.LatLng(coord[0],coord[1])

            };
            map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);
            marker = new google.maps.Marker(
            {
                map: map,
                draggable: false,
                position: new google.maps.LatLng(coord[0], coord[1])

            });


        }

    // redirect to nofeed
    checkIfMainFeedEmpty();

    });

};

