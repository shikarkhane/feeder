function getFeedUrl(){
            var from_datetime = window.pageload_utctime;
            var q_page_size = 10;
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

			var path = window.servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize
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

                    if (! ( $.cookie('subscribed')) ){

					    addSubscribePost($('#main-feed'));
					}
							

		    })
		     .always(function() {
                checkIfMainFeedEmpty();
                $('#in-progress-wheel').addClass('hide');
            });


};
