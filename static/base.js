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



