$(document).on('click', "#add-category", function() {
        var newcategory = $('#txt-category').val();
        url = 'backoffice/category/' + newcategory + '/';
        var jqxhr = $.post( $.cookie('myservername') + url );
        location.reload();
	});

$(document).on('click', "li > span.delete-category", function() {
        var delcategory = $(this).siblings('span.cls_category_name').html();
        console.log(delcategory);
        url = 'backoffice/category/' + delcategory + '/';
        $.ajax({
                url: $.cookie('myservername') + url,
                type: 'DELETE',
                success: function(result) {
                    console.log('Category ' + delcategory + ' was deleted');
                    location.reload();
                }
            });
	});

