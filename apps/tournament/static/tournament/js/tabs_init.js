var selected_tabs = null;

$(document).ready(function() {
    var tabs = $('.round_tabs');
    tabs.change(function(){
        selected_tabs.css('display', 'none');
        selected_tabs = $('#' + $(this).val());
        selected_tabs.css('display', 'block');
    });

    tabs.first().prop('checked', true);
    selected_tabs = $('#' + tabs.first().val());
    selected_tabs.css('display', 'block');
});
