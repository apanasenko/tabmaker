function swap(element, buffer, element_name){
    if (!buffer){
        $(element).css('background', '#fff');
        return element;
    } else {
        var class_id = '.' + element_name + '_id';
        var class_name = '.' + element_name + '_name';
        $(buffer).css('background', $(element).parent().css('background'));

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
    var buffer_chair = null;

    $('.team').click(function(){
        buffer_team = swap(this, buffer_team, 'team');
    });

    $('.chair').click(function(){
        buffer_chair = swap(this, buffer_chair, 'chair');
    });

    $('.place').click(function(){
        buffer_chair = swap(this, buffer_chair, 'place');
    });
});
