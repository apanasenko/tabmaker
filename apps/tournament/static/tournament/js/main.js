var error = 'notification-red';
var success = 'notification-green';
var message = null;


function show_message(data, div_id, message_id){
    if (message !== null){
        message.removeClass();
        message.html('');
    }

    var css_class = error;
    message = $('#' + message_id);
    if (data.status == 'ok') {
        $('#' + div_id).remove();
        css_class = success;
    }
    message.attr('class', css_class).html(data.message);
}


function remove_team(url, id, div_team_id, div_message_id){
    $.post(url, {team_id: id},
        function(data, status){
            show_message(data, div_team_id, div_message_id);
        }
    );
}


function remove_adjudicator(url, id, div_adjudicator_id, div_message_id){
    $.post(url, {user_tournament_rel_id: id},
        function(data, status){
            show_message(data, div_adjudicator_id, div_message_id);
        }
    );
}
