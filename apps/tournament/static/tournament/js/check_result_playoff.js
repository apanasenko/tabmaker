$(document).ready(function(){

    $('#result_form').submit(function(){
        return check_results();
    });

    $('.room').each(function(){
        var room = this;
        var checkbox = $(room).find('.is_check_game_checkbox');
        if (!checkbox.length)
            return;

        var input = $(room).find('.is_check_game_input');
        $(checkbox).prop('checked', parseBool($(input).val()));
        $(checkbox).change(function(){
            activate_input(room, input, checkbox);
        });
        activate_input(room, input, checkbox);
    });
});


function check_results(){
    var checked = true;

    $('.room').each(function(){
        if (!parseBool($(this).find('.is_check_game_input').val()))
            return;

        var checked_room = true;
        var errors_block = $(this).find('.errors');
        var room = this;
        errors_block.html('');
        var team_in_break = 0;
        $.each(['og', 'oo', 'cg', 'co'], function(key, value){
            team_in_break = parseBool($(room).find('.' + value).find('.place').val())
        });

        var need_checked_teams = 2;
        var error_message = '<p>Дальше должны пройти 2 команды</p>';

        if ($('#is_final').val()) {
            need_checked_teams = 1;
            error_message = '<p>В финале должна победить только 1 команда</p>';
        }

        if (team_in_break != need_checked_teams) {
            errors_block.append(error_message);
            checked_room = false;
        }

        checked &= checked_room;
    });

    return checked;
}


function activate_input(room, input, checkbox){
    $(input).val($(checkbox).is(':checked'));
    $(room).find('.place, .reverse_speakers, .game_id').prop(
        'disabled',
        !parseBool($(input).val())
    );
}


function parseBool(str){
    return $.parseJSON(str.toLowerCase())
}
