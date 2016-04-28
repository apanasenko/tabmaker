var id_temp_block = '#temp';
var id_new_question_block = '#new_question';


var class_up_button = '.up';
var class_down_button = '.down';
var class_remove_button = '.remove';
var class_edit_button = '.edit';
var class_save_button = '.save';

var _class_question_block = 'question_block';
var class_question_block = '.' + _class_question_block;
var class_question_show_block = '.show_block';
var class_question_edit_block = '.edit_block';

var class_question_field = '.question';
var class_comment_field = '.comment';
var class_required_field = '.required';
var class_can_remove_field = '.can_remove';
var class_answer_field = '.answer';
var class_star = '.star';

$(document).ready(function(){
    $(id_temp_block).hide();
    init();
    $(class_question_block + ':first').find(class_up_button).hide();
    $(class_question_block + ':last').find(class_down_button).hide();
});


function edit_click(button)
{
    edit_question($(button).parents(class_question_block));
}


function save_click(button)
{
    save_question($(button).parents(class_question_block));
}


function cancel_click(button)
{
    var block = $(button).parents(class_question_block);
    block.find(class_question_show_block).show();
    block.find(class_question_edit_block).hide();
}


function remove_click(button)
{
    var block = $(button).parents(class_question_block);
    var can_remove = block.find(class_can_remove_field).val();
    if (can_remove === '0') {
        alert('ERROR!');
    } else {
        alert('REMOVE!')
    }
}


function swap_visible(block_1, block_2, _class) {
    if (!block_1.find(_class).is(":visible")) {
        block_2.find(_class).hide();
        block_1.find(_class).show();
    }
}


function down_click(button)
{
    var block = $(button).parents(class_question_block);
    var next_block = block.next();
    if (next_block.hasClass(_class_question_block)) {
        block.insertAfter(next_block);
        swap_visible(next_block, block, class_down_button);
        swap_visible(block, next_block, class_up_button);
    } else {
        alert('Ниже нельзя, вопрос уже последний');
    }
}


function up_click(button)
{
    var block = $(button).parents(class_question_block);
    var prev_block = block.prev();
    if (prev_block.hasClass(_class_question_block)) {
        block.insertBefore(prev_block);
        swap_visible(prev_block, block, class_up_button);
        swap_visible(block, prev_block, class_down_button);
    } else {
        alert('Выше нельзя, вопрос уже первый');
    }
}


function add_question()
{
    edit_question(generate_question_block(0, 'Новый вопрос', '', '0', '1'));
}


function set_values(block, question, comment, required)
{
    block.find(class_question_field).text(question);
    block.find(class_comment_field).text(comment);
    block.find(class_required_field).val(required);
    if (required  === '1') {
        block.find(class_star).show();
    } else {
        block.find(class_star).hide();
    }
}


function generate_question_block(id, question, comment, required, can_remove)
{
    var new_block = $(id_temp_block).clone();

    new_block.insertBefore($(id_new_question_block));
    new_block.attr('id', id);
    new_block.addClass(_class_question_block);

    set_values(new_block.find(class_question_show_block), question, comment, required);

    new_block.find(class_can_remove_field).val(can_remove);
    if (can_remove === '0') {
        new_block.find(class_remove_button).hide();
    }

    new_block.show();
    new_block.find(class_question_edit_block).hide();

    return new_block;
}


function edit_question(block)
{
    var show_block = block.find(class_question_show_block);
    var edit_block = block.find(class_question_edit_block);

    var is_required = show_block.find(class_required_field).val() === '1';
    var can_remove = show_block.find(class_can_remove_field).val() === '1';

    edit_block.find(class_question_field).val(show_block.find(class_question_field).text());
    edit_block.find(class_comment_field).val(show_block.find(class_comment_field).text());

    edit_block.find(class_required_field).prop('checked', is_required);
    edit_block.find(class_required_field).prop('disabled', !can_remove);

    show_block.hide();
    edit_block.show();
}


function save_question(block)
{
    var show_block = block.find(class_question_show_block);
    var edit_block = block.find(class_question_edit_block);

    var question = edit_block.find(class_question_field).val();
    var comment = edit_block.find(class_comment_field).val();
    var is_required = edit_block.find(class_required_field).is(':checked') ? "1" : "0";

    set_values(show_block, question, comment, is_required);

    show_block.show();
    edit_block.hide();
}
