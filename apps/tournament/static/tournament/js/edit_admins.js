$(document).ready(function(){
    $('#temp').hide();
    init();
});


function generate_admin_block(name, rel_id){
    var new_block = $('#temp').clone();
    new_block.insertBefore($('#new_admin'));
    new_block.find('#rel_id').val(rel_id);
    new_block.find('.admin_name').html(name);
    new_block.attr('id', rel_id);
    new_block.show();
}


function remove_admin(block, url){
    var admin_block = $(block).parents('.admin');
    $.post(
        url,
        {
            rel_id: admin_block.find("#rel_id").val()
        },
        function(data, status){
            admin_block.find('.errors').html(data.message);
            if (data.status == 'ok'){
                admin_block.remove();
            }
        }
    );
}


function improve_to_owner(block, url, redirect_to){
    var admin_block = $(block).parents('.admin');
    $.post(
        url,
        {
            rel_id: admin_block.find("#rel_id").val()
        },
        function(data, status){
            if (data.status == 'ok'){
                location.href = redirect_to;
            } else {
                admin_block.find('.errors').html(data.message);
            }
        }
    );
}


function save_admin(url){
    var new_admin_block = $('#new_admin');
    var name_input = new_admin_block.find('#add_admin_input');
    $.post(
        url,
        {
            email: name_input.val()
        },
        function(data, status){
            if (data.status == 'bad'){
                new_admin_block.find('.errors').html(data.message);
            } else {
                generate_admin_block(data.message.name, data.message.rel_id);
                name_input.val('');
            }
        }
    );
}
