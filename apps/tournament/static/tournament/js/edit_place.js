$(document).ready(function(){
    $('#temp').hide();
    $('#new_place .errors').hide();

    init();
    $('.place_checkbox').change(function(){
        activated_place(this);
    });
    update_button();
});


function parseBool(str){
    return $.parseJSON(str.toLowerCase())
}


function update_button(){
    if ($('.place_checkbox:checked').length >= $('#places_need').val()){
        $('#check_warning').hide();
        $('#check_button').prop('disabled', false);
    } else {
        $('#check_warning').show();
        $('#check_button').prop('disabled', true);
    }
}


function generate_place_block(name, id, is_active){
    var new_block = $('#temp').clone();
    new_block.insertAfter($('#new_place'));
    new_block.find('#place_id').val(id);
    new_block.find('.place_name').html(name);
    new_block.attr('id', id);
    new_block.find('.place_checkbox').prop('checked', is_active);
    new_block.find('.place_checkbox').change(function(){
        activated_place(this);
    });
    new_block.show();
    update_button();
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
            update_button();
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
            update_button();
        }
    );
}


function save_place(url){
    var new_place_block = $('#new_place');
    var input = new_place_block.find('#add_place_input');
    new_place_block.find('.errors').hide();
    $.post(
        url,
        {
            place: input.val()
        },
        function(data, status){
            if (data.status == 'bad'){
                new_place_block.find('.errors').html(data.message).show();
            } else {
                generate_place_block(data.message.name, data.message.place_id, true);
                input.val('');
            }
        }
    );
}


function redirect(url){
    window.location.href = url;
}
