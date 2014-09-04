$(document).ready(function()
{
    checkIphone();
	//GPS TOGGLE 

	$(".gps").click(function()
	{
		$(this).addClass("active");
		$(".gps h6").html("GPS ON");
	});	

    //SUBSCRIBE TOGGLE
    $(".subscribe .icon,.subscribe h4").bind('click',function(e)
    {
        e.stopPropagation();
        if(!$(this).hasClass("active"))
        {
            $(".verticalmenu").addClass("active");        
            $(this).addClass("active");
            $(".emailsubsc").fadeIn();
        }
        else
        {
            $(".verticalmenu").removeClass("active");        
            $(this).removeClass("active");
            $(".emailsubsc").fadeOut();
            if(!$(".trending .icon").hasClass("active"))
            {
                $(".verticalmenu").removeClass("active");        
            }
        }
    });
	//TRENDING TOGGLE
    $(".trending .icon,.trending h4").bind('click',function(e)
    {
        e.stopPropagation();
        if(!$(this).hasClass("active"))
        {
            $(".verticalmenu").addClass("active");        
            $(this).addClass("active");
            $(".trendinglist").delay(400).show();
        }
        else
        {
            
            $(this).removeClass("active");
            $(".trendinglist").delay(400).hide();
            if(!$(".subscribe .icon").hasClass("active"))
            {
                $(".verticalmenu").removeClass("active");        
            }
        }
        
    
    });


	//SETTINGS MENU TOGGLE
	$(".settings,.label").bind('click',function(e)
	{
        e.stopPropagation();
        if($(".settingsMenu").hasClass('active'))
        {
            $("body").animate({right:'0'},400);
            if($(window).width() >= 400)   
            {
                $("header,.verticalmenu").animate({left:'0'},400);
            }
            else
            {
                $("header").animate({left:'0'},400);
            }
        }
        else
        {

            if($('body').width() >= 400)
            {
                $("body").animate({right:'400px'},400);
                $("header,.verticalmenu").animate({left:'-400px'},400);    
            }
            else
            {
                $("body").animate({right:'80%'},400);
                $("header").animate({left:'-80%'},400);
                if($(".verticalmenu").hasClass("opened"))
                {
                    $(".verticalmenu,.horizontalmenu,section,.iphoneBtn").toggleClass("opened");
                }
            }
            
        }
        $(".settingsMenu").toggleClass("active");
        
	});
    
	
});


    $("body").bind('click',function(e)
    {
        if($(e.target).closest('.settingsMenu').length === 0 && $(".settingsMenu").hasClass("active"))
        {
            
            $(".settings").click();
        }
        else
        {
            if($(e.target).closest(".verticalmenu").length === 0)
            {
                $(".subscribe .icon,.subscribe h4").removeClass("active");
                $(".trending .icon").removeClass('active');
                $(".trendinglist").hide();
                $(".verticalmenu").removeClass("active");  
                $(".emailsubsc").fadeOut(); 
                if($(".verticalmenu").hasClass("opened") && $(e.target).closest(".iphoneBtn").length === 0)
                {
                    $(".verticalmenu,.horizontalmenu,section,.iphoneBtn").toggleClass("opened");
                }
            }
        }

    });   


$(".verticalmenu").height($(window).height());


$(window).resize(function()
{
    if($(".settingsMenu").hasClass('active'))
    {
        $("body").animate({right:'0'},400);
        $("header,.verticalmenu").animate({left:'0'},400);    
        $(".settingsMenu").removeClass("active");
    }
    $(".verticalmenu").height($(window).height());
    checkIphone();
});

function checkIphone()
{
    // IF SCREEN LESS THAN 400PX, HIDE SIDEBAR
    if($(window).width() <= 400 && !$(".settings").hasClass("active"))
    {
        $(".verticalmenu").delay(800).addClass("iphone");
        $(".iphoneBtn").show();
    }
    else
    {
        $(".verticalmenu").removeClass("iphone");
        $(".iphoneBtn").hide();
    }
}

$(".iphoneBtn").click(function()
{
    $(".verticalmenu,.horizontalmenu,section,.iphoneBtn").toggleClass("opened");
});




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
            $container.append('<div class="item col-xs-12 col-sm-6 col-md-4 col-lg-3">
                                    <div class="itemcontent">
                                        <div class="photo lazyload" data-original="'+data[i].content_img_url+'"></div>
                                        <div class="profilePhoto lazyload" data-original="'+data[i].user_img_url+'"></div>
                                        <div class="boxpadding">
                                            <div class="'+data[i].social+'-icon"></div>
                                            <a href="#"><div class="more">...</div></a>
                                            <p class="postcontent">'+data[i].text+'</p>
                                            <div class="bottom">
                                                <h5 class="timeago primary"  title="'+formatDate(new Date(data[i].created))+'"></h5>
                                                <div class="like">'+data[i].up_votes+'</div>
                                                <div class="distance">1km</div>
                                            </div>
                                        </div>
                                    </div>
                                    </div></div>').masonry('reloadItems').masonry('layout');
        }
        $(".feed .lazyload:not(.loaded)").lazyload({
            effect : "fadeIn"
        }).addClass("loaded");
        $(".timeago:not(.timeloaded)").timeago().addClass("timeloaded");

        //LIKE TOGGLE

        $(".like:not(.activated)").click(function()
        {
            var count = parseInt($(this).html());
            if($(this).hasClass("liked"))
            {
                $(this).html(count-1);
            }
            else
            {
                $(this).html(count+1);
            }
            $(this).toggleClass("liked");
        }).addClass("activated");

        //LOAD MAP
    
        $(".distance").colorbox({
            maxWidth: "80%",
            maxHeight: "80%",
            html:'<div id="gmap_canvas" style="width:750px; height:500px;"></div>',
            scrolling:false,
            onComplete:function()
            {
                init_map();
            }
        });
        function init_map()
        {
            var myOptions = 
            {
                zoom:14,
                center:new google.maps.LatLng(40.805478,-73.96522499999998),
                mapTypeId: google.maps.MapTypeId.ROADMAP
                
            };
            map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);
            marker = new google.maps.Marker(
            {
                map: map,
                position: new google.maps.LatLng(40.805478, -73.96522499999998)
                    
            });
            
            
        }

        
    });
}


// SETTINGS - pre-define a selection between Lastest first (irs-min) or Popular first (irs-max)
$(".lastestfirst").addClass("active");

//change when clicked
$(".lastestfirst").click(function()
{
    $(this).addClass("active");
    $(".popularfirst").removeClass("active");
});
$(".popularfirst").click(function()
{
    $(this).addClass("active");
    $(".lastestfirst").removeClass("active");
});

//SETTINGS SLIDERS
$(".variable2").ionRangeSlider({
    min: 1,
    max: 30,
    type: 'single',
    hasGrid: false,
    postfix: " days",
    input: $(this).closest(".selectedOpt"),
    hideMinMax:true
});
$(".variable3").ionRangeSlider({
    min: 1,
    max: 9,
    type: 'single',
    hasGrid: false,
    postfix: "km",
    input: $(this).closest(".selectedOpt"),
    hideMinMax:true
});