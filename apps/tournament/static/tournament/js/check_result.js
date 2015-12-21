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

    $('.exist_speaker').each(function () {
        var speaker_1 = $(this).parents('.speaker_1');
        var speaker_2 = $(this).parents('.speaker_2');
        var speaker = speaker_1.length ? speaker_1 : speaker_2;
        var label = $(speaker).find('.speaker_name');
        var input = $(speaker).find('.points_input');
        $(this).change(function(){
            activate_speaker(this, label, input);
        });
        activate_speaker(this, label, input);

    })
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
        var results = {};
        $.each(['og', 'oo', 'cg', 'co'], function(key, value){
            var s1 = $(room).find('.' + value).find('.speaker_1');
            var s2 = $(room).find('.' + value).find('.speaker_2');
            results[value] = {
                place: parseInt($(room).find('.' + value).find('.place').val()),
                speaker_1: [
                    $(s1).find('.exist_speaker').is(':checked'),
                    parseInt($(s1).find('.speaker_1_points').val())
                ],
                speaker_2: [
                    $(s2).find('.exist_speaker').is(':checked'),
                    parseInt($(s2).find('.speaker_2_points').val())
                ]
            };

            results[value].sum = results[value].speaker_1[1] + results[value].speaker_2[1];
            results[value].is_all = results[value].speaker_1[0] && results[value].speaker_2[0];
        });
        var places = [];
        $.each(results, function(key, value){
            places.push(value.place)
        });
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
            var speakers = [];

            $.each(results, function(key, value){
                speakers[value.place] = value;
            });

            $.each([4, 3, 2], function(key, value) {
                for(var i = value - 1; i > 0; i--){

                    if(!speakers[value].is_all || !speakers[i].is_all)
                        continue;

                    if (speakers[value].sum >= speakers[i].sum){
                        checked_room = checked_room && confirm('Сумма спикерских у ' + i.toString() + ' команды должна быть больше чем у ' + value.toString() + ' команды. Уверены, что хотите продолжиь?');
                    }
                }
            });
        }
        checked = checked && checked_room;
    });
    return checked;
}


function activate_input(room, input, checkbox){
    $(input).val($(checkbox).is(':checked'));
    $(room).find('.speaker_1_points, .speaker_2_points, .place, .reverse_speakers, .game_id, .exist_speaker').prop(
        'disabled',
        !parseBool($(input).val())
    );
}


function activate_speaker(checkbox, label, input){
    if ( ! $(checkbox).is(':checked')){
        $(label).attr('style', 'text-decoration:line-through');
        $(input).prop('readonly', true);
        $(input).val('0');
    } else {
        $(label).removeAttr('style');
        $(input).prop('readonly', false);
    }
}


function parseBool(str){
    return $.parseJSON(str.toLowerCase())
}
