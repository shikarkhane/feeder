$(function() {

			if ($.cookie('mysearchradius')){
				$('#searchradius').val($.cookie('mysearchradius'));
			}
			if ($.cookie('mysortbyvotes')==1){
				$('#sortbyvotes').prop('checked', true);
			}
			else{
				$('#sortbyvotes').prop('checked', false);
			}
	});

	$(document).on('click', "#btnsavesettings", function(event){
		event.preventDefault();
		var radius = $('#searchradius').val();
		if($('#sortbyvotes').is(':checked')){
			$.cookie('mysortbyvotes',  1, { path: '/'});
		}
		else{
			$.cookie('mysortbyvotes',  0, { path: '/'});
		}
		if (radius){
			$.cookie('mysearchradius',  radius, { path: '/'});
			}
		else{
			$.cookie('mysearchradius',  10, { path: '/'});
		}
		window.location.replace("/");
	});