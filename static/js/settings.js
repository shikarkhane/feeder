function change_vote_label( flag ){
    if (flag == 1){
        $( "#sort-by" ).text( "Show popular first." );
    }
    else{
        $( "#sort-by" ).text( "Show latest first." );
    }
}

$(function() {
        $( "#search-radius-slider" ).slider({
          range: "max",
          min: 1,
          max: 9,
          value: $.cookie('mysearchradius'),
          slide: function( event, ui ) {
            $( "#search-radius-label" ).text( ui.value );
            $.cookie('mysearchradius',  ui.value, { path: '/'});
          }
        });
        $( "#search-radius-label" ).text( $.cookie('mysearchradius'));

        $( "#sort-by-votes-slider" ).slider({
          range: "max",
          min: 0,
          max: 1,
          step: 1,
          value: $.cookie('mysortbyvotes'),
          slide: function( event, ui ) {
            change_vote_label(ui.value);
            $.cookie('mysortbyvotes',  ui.value, { path: '/'});
          }
        });
        change_vote_label( $.cookie('mysortbyvotes'));

  });
