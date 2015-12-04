$(document).ready(function() {
    var width = $(window).width();

    $('.btn-menu').click(function() {
        if(width < "375px") {
            $('aside').addClass('class_name');
        }
    });
});