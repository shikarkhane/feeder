
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
function getDate30MinFromNow(){
     var date = new Date();
     var minutes = 30;
     date.setTime(date.getTime() + (minutes * 60 * 1000));
     return date;
 };

 function get_url_value(param){
    if(param=(new RegExp('[?&]'+encodeURIComponent(param)+'=([^&]*)')).exec(location.search))
        return decodeURIComponent(param[1]);
};

function isValidEmail( email ){
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
};