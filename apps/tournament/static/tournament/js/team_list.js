var lastInfoBlock = null;

function update_team_status(url, select, team_tournament_rel_id, message_block_id){

    if (lastInfoBlock){
        lastInfoBlock.html(null);
    }
    $.post(
        url,
        {
            team_tournament_rel_id: team_tournament_rel_id,
            new_role_id: select.value
        },
        function(data, status){
            lastInfoBlock = $('#' + message_block_id);
            lastInfoBlock.html(data.message);
            if (data.status == 'bad'){
                load_value(select);
            } else {
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
