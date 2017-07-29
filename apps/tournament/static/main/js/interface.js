// TODO настроить формат даты, который уходит из формы после включения js-пикера и включить пикеры

// показать и скрыть баннер
$(function() {
    $('.banner__close').click(function() {
        $('.banner').hide();
    });
});

// поведение табов
$(document).ready(function () {

    $('.accordion-tabs').each(function(index) {
        $(this).children('li').find('.is-active').next().addClass('is-open').show();
    });

    $('.accordion-tabs').on('click', 'li > a.tab-link', function(event) {
        event.preventDefault();

        if (!$(this).hasClass('is-active')) {
            var accordionTabs = $(this).closest('.accordion-tabs');
            accordionTabs.find('.is-open').removeClass('is-open').hide();
            $(this).next().toggleClass('is-open').toggle();
            accordionTabs.find('.is-active').removeClass('is-active');
            $(this).addClass('is-active');
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

$(document).ready(function() {
    $('.burger-menu').hide();
    $('.burger__button').click(function () {
        $('.burger-menu').toggle();
    });
});

$(document).ready(function() {
    if (!Cookies.get('hidden_advent_banner')) {
        $('.advert').show();
        $('.advert__close').click(function () {
            Cookies.set('hidden_advent_banner', 1,  { expires: 1 });
            $('.advert').hide();
        });
    }
});

