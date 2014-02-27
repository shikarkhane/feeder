

function peekFromBottomOfScreen(object){
     var viewportWidth = jQuery(window).width(),
            viewportHeight = jQuery(window).height(),
            $foo = object,
            elWidth = $foo.width(),
            elHeight = $foo.height(),
            elOffset = $foo.offset();

        jQuery(window)
            .scrollTop(elOffset.top - (viewportHeight/2));

};
