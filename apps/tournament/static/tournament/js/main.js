    $.post(url, {id: id},
function remove_team(url, id, div_team_id, div_errors_id){
        function(data, status){
            if (data.status == 'ok') {
                $('#' + div_team_id).html(data.message)
            } else {
                $('#' + div_errors_id).html(data.message)
            }
        }
    );
}
