$(document).on('click', "#add-category", function() {
        var newcategory = $('#txt-category').val();
        url = 'backoffice/category/' + newcategory + '/';
        var jqxhr = $.post(get_servername_from_url() + url );

	});

