$(document).ready(function() {
    var width = $(window).width();
    if(width < '641' || width < '769' ) {
        $('aside').hide();
        $('.burger-icon').click(function() {
            if($('aside').is(':hidden')) {
                $('aside').slideDown('fast');
            } else {
                $('aside').slideUp('fast');
            }
        });
    }
});

$(function() {
    $('.b-banner__close').click(function() {
        $('.b-banner-red, .b-banner-yellow, .b-banner-green').hide();
    });
});

$(function() {
    $('.b-window__close').click(function() {
        $('.b-window-red, .b-window-yellow, .b-window-green').hide();
    });
});