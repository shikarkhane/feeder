function pad(num) {
    return ("0" + num).slice(-2);
};

function formatDate(d) {
    return [d.getUTCFullYear(), 
            pad(d.getUTCMonth() + 1), 
            pad(d.getUTCDate())].join("-") + "T" + 
           [pad(d.getUTCHours()), 
            pad(d.getUTCMinutes()), 
            pad(d.getUTCSeconds())].join(":") + "Z";
};

function getAndRenderData(path){
		  	var result = $.get( path, function( data ) {
					var posts = $.parseJSON(data);
					$.each(posts, function(){
							if (this.post_id){
							$('#main-feed').append($('<div/>',{
											    'id'    : this.post_id,
											    'class' : 'main-post row-fluid panel-body breadcrumb'
											}));
							if (!(this.content_img_url == null)){
								$('#' + this.post_id).addClass("clickable_object");
							}
							$('#' + this.post_id).append($('<div/>',{
											    'class' : 'content_link',
											    html : this.content_img_url
											}));
							$('#' + this.post_id).append($('<div/>',{
											    'class' : 'span1',
											    html : '<img src="' + this.user_img_url + '" class="img-responsive"/>'
											}));
							$('#' + this.post_id).append($('<div/>',{
											    'class' : 'span10',
											    html : this.text
											}));
							$('#' + this.post_id).append($('<div/>',{
											    'class' : 'span1 elapsed_time',
											    html : '<span class="x_minutes_ago badge">' + moment(formatDate(new Date(this.created)), "YYYY-MM-DDTHH:mm:ssZ").fromNow() + '</span>'
											}));
						}
							
					    });
				});
};

function getFeedData(q_pagesize, mylat, mylon, fromposition, myfiltertags){
			var path = window.servername + "from/" + fromposition + "/pagesize/" + q_pagesize + "/";
	  		if (!($.cookie('MyLat') == null)){			  				
	    			path = window.servername +  mylat + "/" +  mylon + "/from/" + fromposition + "/pagesize/" + q_pagesize + "/";
	    		}
	    	if (myfiltertags){
	    		path = path + "tags/" + myfiltertags + "/";
	    	}
			getAndRenderData(path);
			handlePageNumber(1, q_pagesize);
};



function couldntFetchPosition(msg){
		alert('Location not found!\n Allow browser to access location services and try again.' + msg );
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



