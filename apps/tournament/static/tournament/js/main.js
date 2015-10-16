function show_message(data, div_id, errors_id){
    if (data.status == 'ok') {
        $('#' + div_id).html(data.message)
    } else {
        $('#' + errors_id).html(data.message)
    }
}


function remove_team(url, id, div_team_id, div_errors_id){
    $.post(url, {team_id: id},
        function(data, status){
            show_message(data, div_team_id, div_errors_id);
        }
    );
}


function remove_adjudicator(url, id, div_adjudicator_id, div_errors_id){
    $.post(url, {user_tournament_rel_id: id},
        function(data, status){
            show_message(data, div_adjudicator_id, div_errors_id);
        }
    );
}
