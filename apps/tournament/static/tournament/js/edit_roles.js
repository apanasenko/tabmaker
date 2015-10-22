var lastInfoBlock = null;

function update_status(url, select, team_tournament_rel_id, message_block_id){

    if (lastInfoBlock){
        lastInfoBlock.html(null);
    }
    $.post(
        url,
        {
            rel_id: team_tournament_rel_id,
            new_role_id: select.value
        },
        function(data, status){
            lastInfoBlock = $('#' + message_block_id);
            lastInfoBlock.html(data.message);
            if (data.status == 'bad'){
                load_value(select);
            } else {
                update_info_block(select.oldValue, -1);
                update_info_block(select.value, 1);
                save_value(select);
            }
        }
    );
}
function on_focus(select){
    $(select).blur(function(){load_value(select)});
    save_value(select);
}

function save_value(select){
    select.oldValue = select.value;
}

function load_value(select){
    $(select).val(select.oldValue);
}

function update_info_block(id, value){
    var a = $('div #message #' + id);
    a.html(parseInt(a.html()) + value);

    var b = $('#member_id');
    var c = $('#chair_id');
    if (b && id == $(b).val()){
        if (parseInt(a.html()) % 4 == 0){
            $('#check_warning').hide();
            $('#check_button').prop('disabled', false);
        } else {
            $('#check_warning').show();
            $('#check_button').prop('disabled', true);
        }
    } else if (c && id == $(c).val()) {
        if (parseInt(a.html()) >= parseInt($('#chair_need').val())) {
            $('#check_warning').hide();
            $('#check_button').prop('disabled', false);
        } else {
            $('#check_warning').show();
            $('#check_button').prop('disabled', true);
        }
    }
}

$(document).ready(function(){
    $("select.roles").each(function(){
        update_info_block(this.value, 1)
    })
});

function redirect(url){
    window.location.href = url;
}
