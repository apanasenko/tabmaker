$(document).ready(function() {
    var width = $(window).width();
    if(width < '769' ) {
        $('aside').hide();
        $('.burger-icon').click(function() {
            if($('aside').is(':hidden')) {
                $('aside').slideDown('fast');
            } else {
                $('aside').slideUp('fast');
            }
        });
    }

    if(window.location.pathname == '/') {
        $('#page_title').hide();
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

$(document).ready(function() {
  $(".dropdown-button").click(function() {
    var $button, $menu;
    $button = $(this);
    $menu = $button.siblings(".dropdown-menu");
    $menu.toggleClass("show-menu");
    $menu.children("li").click(function() {
      $menu.removeClass("show-menu");
    });
  });
});

// $(document).ready(function() {
//     $('.datepicker').pickadate();
//     $('.timepicker').pickatime();
// });

// новая верстка табов

$(document).ready(function () {
  $('.accordion-tabs').each(function(index) {
    $(this).children('li').first().children('a').addClass('is-active').next().addClass('is-open').show();
  });
  $('.accordion-tabs').on('click', 'li > a.tab-link', function(event) {
    if (!$(this).hasClass('is-active')) {
      event.preventDefault();
      var accordionTabs = $(this).closest('.accordion-tabs');
      accordionTabs.find('.is-open').removeClass('is-open').hide();

      $(this).next().toggleClass('is-open').toggle();
      accordionTabs.find('.is-active').removeClass('is-active');
      $(this).addClass('is-active');
    } else {
      event.preventDefault();
    }
  });
});
