function save_adjudicator(url){
    var new_admin_block = $('#new_adjudicator');
    var name_input = new_admin_block.find('#add_adjudicator_input');
    $.post(
        url,
        {
            email: name_input.val()
        },
        function(data, status){
            new_admin_block.find('.errors').html(data.message);
            if (data.status == 'ok'){
                name_input.val('');
                location.reload();
            }
        }
    );
}
