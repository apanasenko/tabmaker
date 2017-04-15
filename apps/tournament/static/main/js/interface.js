// TODO настроить формат даты, который уходит из формы после включения js-пикера и включить пикеры

// показать и скрыть баннер

$(function() {
    $('.b-banner__close').click(function() {
        $('.b-banner-red, .b-banner-yellow, .b-banner-green').hide();
    });
});




// поведение табов

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




// показ табов

$(document).ready(function() {
    $('.menu-item').click(function () {
        var menuItem = $(this).find('.dropdown-content');
        $('.dropdown-content').hide();
        menuItem.toggle();
    });
});
