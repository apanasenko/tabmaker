var selected_block_css = 'b-edit__swap';

function swap(element, buffer, element_name){
    if (!buffer){
        $(element).addClass(selected_block_css);
        return element;
    } else {
        var class_id = '.' + element_name + '_id';
        var class_name = '.' + element_name + '_name';
        $(buffer).removeClass(selected_block_css);

        var team_name = $(element).find(class_name).html();
        var team_id = $(element).find(class_id).val();

        $(element).find(class_name).html($(buffer).find(class_name).html());
        $(buffer).find(class_name).html(team_name);

        $(element).find(class_id).val($(buffer).find(class_id).val());
        $(buffer).find(class_id).val(team_id);

        return null;
    }

}

$(document).ready(function() {
    var buffer_team = null;

    $('.team').click(function(){
        buffer_team = swap(this, buffer_team, 'team');
    });

    swap_in_select_init('chair');
    swap_in_select_init('place');
});


function swap_in_select_init(block_name){
    var class_name = '.' + block_name;
    var chair_select = $(class_name + '_select');
    var prefix = block_name+ '_select_id_';
    chair_select.each(function(){
        $(this).attr('id', prefix + $(this).val());
    });

    chair_select.change(function(){
        var cur_select = $(this);
        var other_select = $('#' + prefix + cur_select.val());
        if (other_select) {
            var last_id = $(this).parents(class_name).find(class_name + '_id').val();
            other_select.parents(class_name).find(class_name + '_id').val(last_id);
            other_select.val(last_id);
            other_select.attr('id', prefix + other_select.val());
        }
        cur_select.parents(class_name).find(class_name + '_id').val(cur_select.val());
        cur_select.attr('id', prefix + cur_select.val());
    });
}
