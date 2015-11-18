$(document).ready(function(){
    $('#temp').hide();

    init();
    $('.place_checkbox').change(function(){
        activated_place(this);
    });
});


function parseBool(str){
    return $.parseJSON(str.toLowerCase())
}


function generate_place_block(name, id, is_active){
    var new_block = $('#temp').clone();
    new_block.insertBefore($('#new_place'));
    new_block.find('#place_id').val(id);
    new_block.find('.place_name').html(name);
    new_block.attr('id', id);
    new_block.find('.place_checkbox').prop('checked', is_active);
    new_block.show();
}


function remove_place(block, url){
    var place_block = $(block).parents('.place');
    $.post(
        url,
        {
            id: place_block.find("#place_id").val()
        },
        function(data, status){
            place_block.find('.errors').html(data.message);
            if (data.status == 'ok'){
                place_block.remove();
            }
        }
    );
}


function activated_place(block){
    var place_block = $(block).parents('.place');
    $.post(
        $('#place_update_url').val(),
        {
            place_id: place_block.find("#place_id").val(),
            is_active: $(block).is(':checked')
        },
        function(data, status){
            if (data.status == 'ok'){
                $(block).prop('checked', data.message);
            } else {
                place_block.find('.errors').html(data.message);
            }
        }
    );
}


function save_place(url){
    var new_place_block = $('#new_place');
    var input = new_place_block.find('#add_place_input');
    new_place_block.find('.errors').html('');
    $.post(
        url,
        {
            place: input.val()
        },
        function(data, status){
            if (data.status == 'bad'){
                new_place_block.find('.errors').html(data.message);
            } else {
                generate_place_block(data.message.name, data.message.place_id, true);
                input.val('');
            }
        }
    );
}