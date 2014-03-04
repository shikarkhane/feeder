function setFromPosition(){
		if (($.cookie('FromPosition') == null)||($.cookie('FromPosition') == "NaN")){
			$.cookie('FromPosition', 0, { path: '/'});
		};
	};

function getFeedData(from_datetime, q_pagesize, mylat, mylon, fromposition, myfiltertags, mysearchradius, mysortbyvotes){
			var path = window.servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize + "/radius/" + mysearchradius + '/sort/' + mysortbyvotes + '/';
			var popular_path = window.servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/4/radius/" + mysearchradius + '/sort/' + mysortbyvotes + '/';
	  		if (!($.cookie('MyLat') == null)){			  				
	    			path = path +  "location/" + mylat + "/" +  mylon + "/";
	    			popular_path = popular_path +  "location/" + mylat + "/" +  mylon + "/";
	    		}
	    	if (myfiltertags){
	    		path = path + "tags/" + myfiltertags + "/";
	    		popular_path = popular_path + "tags/" + myfiltertags + "/";
	    	}
	    	popular_path = popular_path + "source/instagram/";
			getAndRenderData(path, popular_path);
			handlePageNumber(1, q_pagesize);

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

function addNoFeedAvailable(){
		$('#main-feed').html($('<div/>',{
		                                'id' : 'warning-nofeed',
                                        'class' : 'label label-warning',
                                        html : ' No data available right now. Check again in a bit.'
                                    }));
        if ( ! ($.cookie('subscribed'))){
            $('#div-subscribe').removeClass('hide');
        }
};

function checkIfMainFeedEmpty(){
    if ( $('#main-feed').children('div.main-post').length > 0 ) {
         //remove nofeed warning
         $('#warning-nofeed').remove();
    }
    else{
        addNoFeedAvailable();
    }
};
function getAndRenderData(path, popular_path){
            moment.lang('en', {
                relativeTime : {
                    future: "in %s",
                    past:   "%s",
                    s:  "s",
                    m:  "a min",
                    mm: "%d min",
                    h:  "an hr",
                    hh: "%d hr",
                    d:  "a day",
                    dd: "%d d",
                    M:  "a mon",
                    MM: "%d months",
                    y:  "a year",
                    yy: "%d years"
                }
            });

            $('#in-progress-wheel').removeClass('hide');
            var pop_result = $.get( popular_path, function( data ) {
					var posts = $.parseJSON(data);
					if (posts[0]){
					    var id_to_use = 'popular' + posts[0].doc_id;
                        $('#main-feed').append($('<div/>',{
                                            'id'    : id_to_use,
                                            'class' : 'main-post panel-body breadcrumb'
                                        }));
                        $('#' + id_to_use).append($('<div/>',{
                                            'class' : 'row popular'
                                        }));
                        $.each(posts, function(){
                               $('#' + id_to_use + " > div.popular").append($('<div/>',{
                                        'class' : 'col-xs-6 col-md-3',
                                        'html' : '<a href="/post/' + this.doc_id + '/" class="thumbnail"><img src="'
                                        + this.content_img_url + '" class="img-responsive"/></a>'
                                                }));
                        });
					}
            });
		  	var result = $.get( path, function( data ) {
					var posts = $.parseJSON(data);
					var id_to_use;
					var id_to_check_duplicates;
					$.each(posts, function(){
					        id_to_use = String(this.doc_id);
					        id_to_check_duplicates = this.source + String(this.post_id);
							if ((id_to_use) && ($("#" + id_to_check_duplicates).length == 0)){
							$('#main-feed').append($('<div/>',{
											    'id'    : id_to_use,
											    'class' : 'main-post panel-body breadcrumb'
											}));
							$('#' + id_to_use).append($('<div/>',{
							                    'id'    : id_to_check_duplicates,
											    'class' : 'content_link',
											    html : this.content_img_url
											}));
							$('#' + id_to_use).append($('<div/>',{
							                    'class' : 'btn btn-default coord',
											    html : this.coord
											}));

							$('<div/>',{
								'class' : 'row post-top'
							}).appendTo('#' + id_to_use)
								.append($('<div/>',{
								    'class' : 'col-md-1 pull-right',
								    'html' : '<img src="static/images/' + this.source + '_post.png" class="img-responsive content-provider-logo pull-right"/>'
											}))
								.append($('<div/>',{
											    'class' : 'col-md-1 pull-right elapsed_time',
											    html : '<span class="x_minutes_ago badge">' + moment(formatDate(new Date(this.created)), "YYYY-MM-DDTHH:mm:ssZ").fromNow() + '</span>'
											}))
								.append($('<div/>',{
											    'class' : 'col-md-3',
											    html : '<a class="btn btn-primary" target="_blank" href="' + this.user_profile_url + '"><img src="' + this.user_img_url + '" class="profile-img img-responsive"/></a>'
											}))
								.append($('<div/>',{
											    'class' : 'col-md-7',
											    html : '<p class="text-left text">' + this.text + '</p>'
											}));
							;

							$('<div/>',{
								'class' : 'post-bottom btn-group btn-group-justified'
							}).appendTo('#' + id_to_use)
								.append($('<a/>',{
												'type' : 'button',
											    'class' : 'btn btn-default post-like',
											    html : '<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp;' + this.up_votes
											}))
								.append($('<a/>',{
													'type' : 'button',
												    'class' : 'btn btn-default',
												    'href' : '/post/' + id_to_use + '/',
												    html : '<span class="glyphicon glyphicon-folder-open"></span>'
												}))
								.append($('<a/>',{
								                'type' : 'button',
							                    'class' : 'btn btn-default placename truncate',
											    html : this.place_name
											}))
							;
							}
					});
							

		    })
		     .always(function() {
                checkIfMainFeedEmpty();
                $('#in-progress-wheel').addClass('hide');
            });


};

var url = window.location.pathname;
	var servername = 'http://' + $('<a>').prop('href', url).prop('hostname')  + '/';
	if (!($('<a>').prop('href', url).prop('port') == null)){
		servername = 'http://' + $('<a>').prop('href', url).prop('hostname') + ':' + $('<a>').prop('href', url).prop('port') + '/';
        $.cookie('myservername', servername, { path: '/'});
	}
	var default_pagesize = new Number(10);
	var pageload_utctime = moment.utc().valueOf();

    $(function() {
        setLocalityName();
    });


	function setCoordinateCookie(position){
            //alert('set coord');
		  	$.cookie('MyLat', position.coords.latitude, { expires:getDate30MinFromNow(), path: '/'}); // Storing latitude value
			$.cookie('MyLon', position.coords.longitude, { expires:getDate30MinFromNow(), path: '/'}); // Storing longitude value
			$("#main-feed").empty();
			$.cookie('FromPosition', 0, { path: '/'});
			getFeedData(window.pageload_utctime, window.default_pagesize*3, $.cookie('MyLat'), $.cookie('MyLon'),
			$.cookie('FromPosition'), $.cookie('myFilterTags'), $.cookie('mysearchradius'), $.cookie('mysortbyvotes'));
            reverseLookupLocality($.cookie('MyLat'), $.cookie('MyLon'));
		 };
	function couldntFetchPosition(msg){
			//alert('Location not found!\n Allow browser to access location services and try again.\nShowing random data!');
            setLocationBasedOnIpaddress();
            $('#in-progress-wheel').addClass('hide');
	};

	$(function() {
			if (!($.cookie('FirstTimeUser'))){
				window.location.replace("/we/firsttimeuser/");
			};

			$.cookie('FromPosition', 0, { path: '/'});
			$.cookie('myFilterTags', '', { path: '/'});
			if (!($.cookie('mysearchradius'))){
				$.cookie('mysearchradius', 9, { path: '/'});
			}
			if (!($.cookie('mysortbyvotes'))){
				$.cookie('mysortbyvotes', 0, { path: '/'});
			}

			window.pageload_utctime = moment.utc().valueOf();

			if (!($.cookie('MyLat')) && navigator.geolocation){
                $('#in-progress-wheel').removeClass('hide');
                navigator.geolocation.getCurrentPosition(setCoordinateCookie, couldntFetchPosition, {timeout:5000});
			}
			else{
				getFeedData(window.pageload_utctime, window.default_pagesize*3, $.cookie('MyLat'), $.cookie('MyLon'),
					$.cookie('FromPosition'), $.cookie('myFilterTags'), $.cookie('mysearchradius'), $.cookie('mysortbyvotes'));

			};
	});

	$.fn.isOnScreen = function(){

	    var win = $(window);

	    var viewport = {
	        top : win.scrollTop(),
	        left : win.scrollLeft()
	    };
	    viewport.right = viewport.left + win.width();
	    viewport.bottom = viewport.top + win.height();

	    var bounds = this.offset();
	    bounds.right = bounds.left + this.outerWidth();
	    bounds.bottom = bounds.top + this.outerHeight();

	    return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));

	};

	$(window).scroll(function(){
		if(($('#footer').isOnScreen())){
							getFeedData(window.pageload_utctime, window.default_pagesize, $.cookie('MyLat'), $.cookie('MyLon'),
							$.cookie('FromPosition'), $.cookie('myFilterTags'), $.cookie('mysearchradius'), $.cookie('mysortbyvotes'));
						}
	});


	$(document).on('click', "a.post-link", function() {
		var content_url = $(this).closest("div.post-bottom").siblings("div.content_link").text();
		window.open(content_url);
  		return false;
	});



    $(document).on('click', "a.placename", function() {
        $('#in-progress-wheel').removeClass('hide');
		var mainpost_id = $(this).closest("div.main-post");
        var coordinates = $(mainpost_id).find("div.coord").text();

        if ($(this).hasClass('btn-success')){
                mainpost_id.find("div.mapCanvas").remove();
                $(this).addClass('btn-default').removeClass('btn-success');
                $('#in-progress-wheel').addClass('hide');
                return;
            };
        $(this).addClass('btn-success').removeClass('btn-default');

        insert_map(mainpost_id, coordinates);
        google.maps.event.addDomListener(window, 'resize', insert_map);
        google.maps.event.addDomListener(window, 'load', insert_map);
        peekFromBottomOfScreen(mainpost_id.find("div.mapCanvas"));
        $('#in-progress-wheel').addClass('hide');
	});

	$(document).on('click', "#btnfiltertags", function(event){
		event.preventDefault();
        $('#in-progress-wheel').removeClass('hide');
		var filterstring = $('#txtfiltertags').val().replace(/\s+/g, '');
		var myencodedfiltertags = encodeURIComponent(filterstring);
		$.cookie('myFilterTags',  myencodedfiltertags, { expires: getDate30MinFromNow(), path: '/'});
		$("#main-feed").empty();
		$.cookie('FromPosition', 0, { path: '/'});
		window.pageload_utctime = moment.utc().valueOf();
		getFeedData(window.pageload_utctime, window.default_pagesize*3, $.cookie('MyLat'), $.cookie('MyLon'),
		$.cookie('FromPosition'), $.cookie('myFilterTags'), $.cookie('mysearchradius'), $.cookie('mysortbyvotes'));

        $('button.navbar-toggle').trigger('click');
        $('#in-progress-wheel').addClass('hide');

	});

$(function() {
    $('#home-brand > span').attr('class', 'glyphicon glyphicon-home');
    $('#home-brand').attr('href', '/');
});