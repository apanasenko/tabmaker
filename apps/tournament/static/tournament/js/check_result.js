$(document).ready(function(){
    $('#result_form').submit(function(){
        return check_results()
    });
});


function get_sum_speaker(block, position){
    var team =$(block).find('.' + position);
    return parseInt($(team).find('.speaker_1_points').val()) + parseInt($(team).find('.speaker_2_points').val())
}


function check_results(){
    var checked = true;
    $('.room').each(function(){
        if (!parseBool($(this).find('.is_check_game_input').val()))
            return;

        var checked_room = true;
        var errors_block = $(this).find('.errors');
        errors_block.html('');
        var og = parseInt($(this).find('.og').find('.place').val());
        var oo = parseInt($(this).find('.oo').find('.place').val());
        var cg = parseInt($(this).find('.cg').find('.place').val());
        var co = parseInt($(this).find('.co').find('.place').val());
        var places = [og, oo, cg, co];
        $.each([1, 2, 3, 4], function(key, value){
            if (places.indexOf(value) == -1){
                errors_block.append('<p>Нет ' + value + ' места</p>');
                checked_room = false;
            }
            if (places.indexOf(value) != places.lastIndexOf(value)){
                errors_block.append('<p>У двух команд ' + value + ' место</p>');
                checked_room = false;
            }
        });
        if (checked_room){
            var speakers_point = {};
            speakers_point[og] = get_sum_speaker(this, 'og');
            speakers_point[oo] = get_sum_speaker(this, 'oo');
            speakers_point[cg] = get_sum_speaker(this, 'cg');
            speakers_point[co] = get_sum_speaker(this, 'co');
            $.each([4, 3, 2], function(key, value) {
                if (speakers_point[value] > speakers_point[value - 1]) {
                    errors_block.append(
                        '<p>Сумма спикерских у ' + (value - 1).toString() + ' команды не должна быть больше чем у ' + value.toString() + ' команды</p>'
                    );
                    checked_room = false;
                }
            });
        }
        checked = checked && checked_room;
    });
    return checked;
}


$(document).ready(function(){
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


function activate_input(room, input, checkbox){
    $(input).val($(checkbox).is(':checked'));
    $(room).find('.speaker_1_points, .speaker_2_points, .place, .reverse_speakers, .game_id').prop(
        'disabled',
        !parseBool($(input).val())
    );
}


function parseBool(str){
    return $.parseJSON(str.toLowerCase())
}
