function getFeedData(from_datetime, q_pagesize, mylat, mylon, fromposition, myfiltertags){
			var path = window.servername + "time/" + from_datetime + "/from/" + fromposition + "/pagesize/" + q_pagesize + "/";
	  		if (!($.cookie('MyLat') == null)){			  				
	    			path = path +  "location/" + mylat + "/" +  mylon + "/";
	    		}
	    	if (myfiltertags){
	    		path = path + "tags/" + myfiltertags + "/";
	    	}
			getAndRenderData(path);
			handlePageNumber(1, q_pagesize);
};



function couldntFetchPosition(msg){
		alert('Location not found!\n Allow browser to access location services and try again.');
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


	
function getAndRenderData(path){
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
							$('<div/>',{
								'class' : 'row post-top'
							}).appendTo('#' + this.post_id)
								.append($('<div/>',{
								    'class' : 'col-md-1 pull-right',
								    'html' : '<img src="static/images/Twitter_logo_blue.png" class="img-responsive content-provider-logo pull-right"/>'
											}))											
								.append($('<div/>',{
											    'class' : 'col-md-3',
											    html : '<img src="' + this.user_img_url + '" class="img-responsive"/>'
											}))
							;
							$('<div/>',{
								'class' : 'row post-middle'
							}).appendTo('#' + this.post_id)
								.append($('<div/>',{
											    'class' : 'col-md-12',
											    html : this.text
											}))											
							;
							$('<div/>',{
								'class' : 'row post-bottom'
							}).appendTo('#' + this.post_id)
								.append($('<div/>',{
											    'class' : 'post-info elapsed_time col-md-4 pull-right',
											    html : '<span class="x_minutes_ago badge">' + moment(formatDate(new Date(this.created)), "YYYY-MM-DDTHH:mm:ssZ").fromNow() + '</span>'
											}))
								.append($('<div/>',{
											    'class' : 'post-actions col-md-8'
											}))
							;
							$('#' + this.post_id + ' > div.post-bottom > div.post-actions').append($('<button/>',{
												'type' : 'button',
											    'class' : 'btn btn-default post-like',
											    html : '<span class="glyphicon glyphicon-thumbs-up"></span>&nbsp;' + this.up_votes
											}));
							if (!(this.content_img_url == null)){
								$('#' + this.post_id + ' > div.post-bottom > div.post-actions').append($('<button/>',{
													'type' : 'button',
												    'class' : 'btn btn-default post-link',
												    html : '<span class="glyphicon glyphicon-link"></span>'
												}));
							}
						}
							
					    });
				});
};

