
$(document).on('click', "li", function(event){
    $('#bo_tabs > li.active').removeClass('active');
    $(this).addClass('active');
});