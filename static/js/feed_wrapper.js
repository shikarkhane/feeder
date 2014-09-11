

var clickHandler = "click";

if('ontouchstart' in document.documentElement){
    clickHandler = "touchstart";
}


function clickSettings(e)
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
            $("body").animate({right:'85%'},400);
            $("header").animate({left:'-85%'},400);
            if($(".verticalmenu").hasClass("opened"))
            {
                $(".verticalmenu,.horizontalmenu,section,.iphoneBtn").toggleClass("opened");
            }
        }
        
    }
    $(".settingsMenu").toggleClass("active");
}


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
    $(".subscribe .icon,.subscribe h4").bind(clickHandler,function(e)
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
    $(".trending .icon,.trending h4").bind(clickHandler,function(e)
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
	$(".settings,.label").bind(clickHandler,function(e)
	{
        clickSettings(e);
        
	});
    

	
});



    $("body").bind(clickHandler,function(e)
    {
        if($(e.target).closest('.settingsMenu').length === 0 && $(".settingsMenu").hasClass("active"))
        {
            
            clickSettings(e);
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



$(window).resize(function()
{
    if($(".settingsMenu").hasClass('active'))
    {
        $("body").animate({right:'0'},400);
        $("header,.verticalmenu").animate({left:'0'},400);    
        $(".settingsMenu").removeClass("active");
    }
    checkIphone();
});

function checkIphone()
{
    // IF SCREEN LESS THAN 400PX, HIDE SIDEBAR
    if($(window).width() <= 400 && !$(".settings").hasClass("active"))
    {
        $(".verticalmenu").delay(400).addClass("iphone");
        $(".iphoneBtn").show();
        
    }
    else
    {
        $(".verticalmenu").removeClass("iphone");
        $(".iphoneBtn").hide();
        $(".verticalmenu").ClassyScroll(
        {
            sliderSize:'50%'
        });
    }
}

$(".iphoneBtn").click(function()
{
    $(".verticalmenu,.horizontalmenu,section,.iphoneBtn").toggleClass("opened");
    if($(".settingsMenu").hasClass("active"))
    {
        $(".settings").click();
    }
});




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

$("div.logo").click(function()
{
    window.location.replace("/");
});

$("h3.terms").click(function()
{
    window.location.replace("/we/terms/");
});
$("h3.advertise").click(function()
{
    window.location.replace("/we/advertise/");
});
$("h3.help").click(function()
{
    window.location.replace("/we/help/");
});
$("h3.privacy").click(function()
{
    window.location.replace("/we/privacy/");
});