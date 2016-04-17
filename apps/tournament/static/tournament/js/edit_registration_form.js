var notification_timeout = 2000;

var response_ok = 'ok';
var response_bad = 'bad';

var class_error_notification = 'notification-red';
var class_success_notification = 'notification-green';

var fail_message = 'Неудалось связаться с сервером. Обновите страницу и попробуйте ещё раз';
var fail_down = 'Ниже нельзя, вопрос уже последний';
var fail_up = 'Выше нельзя, вопрос уже первый';
var undefined_status = 'Неизветсный статус ответа';
var remove_required_field = 'Незьзя удалить обязательный вопрос';

var id_form_input = '#form_id';
var id_new_question_block = '#new_question';
var id_temp_block = '#temp';
var id_url_input = '#url';

var class_up_button = '.up';
var class_down_button = '.down';
var class_remove_button = '.remove';
var class_edit_button = '.edit';
var class_save_button = '.save';

var _class_question_block = 'question_block';
var class_question_block = '.' + _class_question_block;
var class_question_show_block = '.show_block';
var class_question_edit_block = '.edit_block';
var class_notification_block = '.message';
var class_actions_buttons_block = '.actions_buttons';

var class_question_field = '.question';
var class_comment_field = '.comment';
var class_required_field = '.required';
var class_can_remove_field = '.can_remove';
var class_answer_field = '.answer';
var class_star = '.star';

var editable_block = null;

$(document).ready(function(){
    $(id_temp_block).hide();
    init();
    $(class_question_block + ':first').find(class_up_button).hide();
    $(class_question_block + ':last').find(class_down_button).hide();
});


function send(data, block, success, error){
    data.form_id = $(id_form_input).val();
    $.post(
        $(id_url_input).val(),
        data,
        function(data){
            if (data.status === response_ok){
                success(data);
            } else if (data.status === response_bad){
                error(data);
            } else {
                show_notification(block, response_bad, undefined_status);
            }
        }
    ).fail(function(){
        show_notification(block, response_bad, fail_message);
    });
}


function show_notification(block, status, message){
    var css_class = status == response_ok ? class_success_notification : class_error_notification;
    var message_block = block.find(class_notification_block);
    message_block.addClass(css_class);
    message_block.text(message);
    message_block.show();
    setTimeout(function() {
        message_block.removeClass(css_class);
        message_block.text('');
        message_block.hide();
    }, notification_timeout);
}


function edit_click(button){
    edit_question($(button).parents(class_question_block));
}


function save_click(button, action){
    save_question($(button).parents(class_question_block), action);
}


function cancel_click(button){
    cancel($(button).parents(class_question_block));
}


function remove_click(button, action){
    var block = $(button).parents(class_question_block);
    var can_remove = block.find(class_can_remove_field).val();
    if (can_remove === '0'){
        show_notification(block, response_bad, remove_required_field);
    } else {
        send(
            {
                question_id: block.attr('id'),
                action: action
            },
            block,
            function(data){
                block.remove();
                $(class_question_block + ':first').find(class_up_button).hide();
                $(class_question_block + ':last').find(class_down_button).hide();
            },
            function(data){
                show_notification(block, data.status, data.message);
            }
        );
    }
}


function swap_visible(block_1, block_2, _class){
    if (!block_1.find(_class).is(":visible")){
        block_2.find(_class).hide();
        block_1.find(_class).show();
    }
}


function down_click(button, action){
    change_editable_block(null);
    var block = $(button).parents(class_question_block);
    var next_block = block.next();
    if (next_block.hasClass(_class_question_block)){
        send(
            {
                question_id: block.attr('id'),
                action: action,
                next_question_id: next_block.attr('id')
            },
            block,
            function(data){
                block.insertAfter(next_block);
                swap_visible(next_block, block, class_down_button);
                swap_visible(block, next_block, class_up_button);
            },
            function(data){
                show_notification(block, data.status, data.message);
            }
        );
    } else {
        show_notification(block, response_bad, fail_down);
    }
}


function up_click(button, action){
    change_editable_block(null);
    var block = $(button).parents(class_question_block);
    var prev_block = block.prev();
    if (prev_block.hasClass(_class_question_block)){
        send(
            {
                question_id: block.attr('id'),
                action: action,
                prev_question_id: prev_block.attr('id')
            },
            block,
            function(data){
                block.insertBefore(prev_block);
                swap_visible(prev_block, block, class_up_button);
                swap_visible(block, prev_block, class_down_button);
            },
            function(data){
                show_notification(block, data.status, data.message);
            }
        );
    } else {
        show_notification(block, response_bad, fail_up);
    }
}


function add_question(){
    var block = generate_question_block(0, 'Новый вопрос', '', '0', '1');
    edit_question(block);
    block.find(class_actions_buttons_block).hide();
    $(id_new_question_block).hide();
}


function set_values(block, question, comment, required){
    block.find(class_question_field).text(question);
    block.find(class_comment_field).text(comment);
    block.find(class_required_field).val(required);
    if (required  === '1'){
        block.find(class_star).show();
    } else {
        block.find(class_star).hide();
    }
}


function generate_question_block(id, question, comment, required, can_remove){
    var new_block = $(id_temp_block).clone();

    new_block.insertBefore($(id_new_question_block));
    new_block.attr('id', id);
    new_block.addClass(_class_question_block);

    set_values(new_block.find(class_question_show_block), question, comment, required);

    new_block.find(class_can_remove_field).val(can_remove);
    if (can_remove === '0'){
        new_block.find(class_remove_button).hide();
    }

    new_block.show();
    new_block.find(class_question_edit_block).hide();
    new_block.find(class_notification_block).hide();

    return new_block;
}


function edit_question(block){
    change_editable_block(block);
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


function save_question(block, action){
    var show_block = block.find(class_question_show_block);
    var edit_block = block.find(class_question_edit_block);

    var question = edit_block.find(class_question_field).val();
    var comment = edit_block.find(class_comment_field).val();
    var is_required = edit_block.find(class_required_field).is(':checked') ? "1" : "0";
    send(
        {
            question_id: block.attr('id'),
            action: action,
            question: question,
            comment: comment,
            is_required: is_required
        },
        block,
        function(data){
            set_values(show_block, question, comment, is_required);
            show_block.show();
            edit_block.hide();
            if (!parseInt(block.attr('id'))){
                block.attr('id', data.message.question_id);
                block.find(class_actions_buttons_block).show();
                swap_visible(block.prev(), block, class_down_button);
                $(id_new_question_block).show();
            }
            //show_notification(block, data.status, data.message.message);
        },
        function(data){
            show_notification(block, data.status, data.message);
        }
    );
}


function cancel(block){
    if (block.attr('id') === '0'){
        block.remove();
        $(id_new_question_block).show();
    } else {
        block.find(class_question_show_block).show();
        block.find(class_question_edit_block).hide();
    }
}


function change_editable_block(new_editable_block){
    if (editable_block) {
        cancel(editable_block);
    }
    editable_block = new_editable_block;
}
