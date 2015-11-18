function save_adjudicator(url){
    var new_adjudicator_block = $('#new_adjudicator');
    var name_input = new_adjudicator_block.find('#add_adjudicator_input');
    new_adjudicator_block.find('.errors').html('');
    $.post(
        url,
        {
            email: name_input.val()
        },
        function(data, status){
            new_adjudicator_block.find('.errors').html(data.message);
            if (data.status == 'ok'){
                name_input.val('');
                location.reload();
            }
        }
    );
}
