function setFromPosition(){
		if (($.cookie('FromPosition') == null)||($.cookie('FromPosition') == "NaN")){
			$.cookie('FromPosition', 0, { path: '/'});
		};
	};

function getFeedData(from_datetime, q_pagesize, mylat, mylon, fromposition, myfiltertags, mysearchradius, mysortbyvotes){
			var path = window.servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize + "/radius/" + mysearchradius + '/sort/' + mysortbyvotes + '/';
	  		if (!($.cookie('MyLat') == null)){			  				
	    			path = path +  "location/" + mylat + "/" +  mylon + "/";
	    		}
	    	if (myfiltertags){
	    		path = path + "tags/" + myfiltertags + "/";
	    	}
			getAndRenderData(path);
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
function getAndRenderData(path){
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

		  	var result = $.get( path, function( data ) {
					var posts = $.parseJSON(data);
					$.each(posts, function(){
							if ((this.post_id) && ($("#" + this.post_id).length == 0)){
							$('#main-feed').append($('<div/>',{
											    'id'    : this.post_id,
											    'class' : 'main-post panel-body breadcrumb'
											}));
							$('#' + this.post_id).append($('<div/>',{
											    'class' : 'content_link',
											    html : this.content_img_url
											}));
							$('#' + this.post_id).append($('<div/>',{
							                    'class' : 'btn btn-default coord',
											    html : this.coord
											}));

							$('<div/>',{
								'class' : 'row post-top'
							}).appendTo('#' + this.post_id)
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
							}).appendTo('#' + this.post_id)
								.append($('<a/>',{
												'type' : 'button',
											    'class' : 'btn btn-default post-like',
											    html : '<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp;' + this.up_votes
											}))
								.append($('<a/>',{
													'type' : 'button',
												    'class' : 'btn btn-default post-link hide',
												    html : '<span class="glyphicon glyphicon-link"></span>'
												}))
								.append($('<a/>',{
								                'type' : 'button',
							                    'class' : 'btn btn-default placename truncate',
											    html : this.place_name
											}))
							;
							if (!(this.content_img_url == null)){
							        $('#' + this.post_id).find('a.post-link').removeClass('hide');
							    };
							}
					});
							

		    })
		     .always(function() {
                checkIfMainFeedEmpty();
                $('#in-progress-wheel').addClass('hide');
            });


};

