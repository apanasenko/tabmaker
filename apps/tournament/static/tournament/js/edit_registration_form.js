function CustomQuestionsEditor($parent_block, form_id, url, up_action, down_action, save_action, remove_action)
{
    var self = this;

    self.notification_timeout = 2000;

    self.response_ok = 'ok';
    self.response_bad = 'bad';

    self.class_error_notification = 'notification-red';
    self.class_success_notification = 'notification-green';

    self.fail_message = 'Неудалось связаться с сервером. Обновите страницу и попробуйте ещё раз';
    self.fail_down = 'Ниже нельзя, вопрос уже последний';
    self.fail_up = 'Выше нельзя, вопрос уже первый';
    self.undefined_status = 'Неизветсный статус ответа';
    self.remove_required_field = 'Незьзя удалить обязательный вопрос';
    self.edit_required_field = 'Незьзя редактировать обязательный вопрос. Он нужен для создания команд';

    self._class_question_block = 'question_block';
    self.class_question_block = '.' + self._class_question_block;
    self.class_question_show_block = '.show_block';
    self.class_question_field = '.question';
    self.class_comment_field = '.comment';
    self.class_required_field = '.required';
    self.class_star = '.star';
    self.class_can_remove_field = '.can_remove';
    self.class_question_edit_block = '.edit_block';
    self.class_notification_block = '.message';
    self.class_actions_buttons_block = '.actions_buttons';

    self.class_up_button = '.up';
    self.class_add_button = '.add';
    self.class_down_button = '.down';
    self.class_edit_button = '.edit';
    self.class_cancel_button = '.cancel';
    self.class_save_button = '.save';
    self.class_remove_button = '.remove';

    self.url = url;
    self.form_id = form_id;
    self.up_action = up_action;
    self.down_action = down_action;
    self.save_action = save_action;
    self.remove_action = remove_action;
    self.$parent_block = $parent_block;
    self.$new_question_block = $parent_block.find('#new_question');
    self.$temp_block = $parent_block.find('#temp');
    self.$editable_block = null;
    self.action_executed = false;


    function set_values($block, question, comment, required){
        $block.find(self.class_question_field).text(question);
        $block.find(self.class_comment_field).text(comment);
        $block.find(self.class_required_field).val(required);
        if (required  === '1'){
            $block.find(self.class_star).show();
        } else {
            $block.find(self.class_star).hide();
        }
    }


    function show_notification($block, status, message){
        var css_class = status == self.response_ok ? self.class_success_notification : self.class_error_notification;
        var $message_block = $block.find(self.class_notification_block);
        $message_block.addClass(css_class);
        $message_block.text(message);
        $message_block.show();
        setTimeout(function() {
            $message_block.removeClass(css_class);
            $message_block.text('');
            $message_block.hide();
        }, self.notification_timeout);
    }


    function change_editable_block($new_editable_block){
        if (self.$editable_block) {
            cancel(self.$editable_block);
        }
        self.$editable_block = $new_editable_block;
    }


    function cancel($block){
        if ($block.attr('id') === '0'){
            $block.remove();
            self.$new_question_block.show();
        } else {
            $block.find(self.class_question_show_block).show();
            $block.find(self.class_question_edit_block).hide();
        }
    }


    function edit_question($block){
        if ($block.find(self.class_can_remove_field).val() === '0'){
            show_notification($block, self.response_bad, self.edit_required_field);
        } else {
            change_editable_block($block);
            var $show_block = $block.find(self.class_question_show_block);
            var $edit_block = $block.find(self.class_question_edit_block);
            $edit_block.find(self.class_question_field).val($show_block.find(self.class_question_field).text());
            $edit_block.find(self.class_comment_field).val($show_block.find(self.class_comment_field).text());
            $edit_block.find(self.class_required_field).prop(
                'checked',
                $show_block.find(self.class_required_field).val() === '1'
            );
            $show_block.hide();
            $edit_block.show();
        }
    }


    function generate_question_block (id, question, comment, required, can_remove){
        var $new_block = self.$temp_block.clone();
        $new_block.insertBefore(self.$new_question_block);
        $new_block.attr('id', id);
        $new_block.addClass(self._class_question_block);
        $new_block.find(self.class_edit_button).click(function () { edit_question($new_block) });
        $new_block.find(self.class_cancel_button).click(function () { cancel($new_block) });
        $new_block.find(self.class_up_button).click(function () { up_click($new_block) });
        $new_block.find(self.class_down_button).click(function () { down_click($new_block) });
        $new_block.find(self.class_save_button).click(function () { save_click($new_block) });
        $new_block.find(self.class_remove_button).click(function () { remove_click($new_block) });

        set_values($new_block.find(self.class_question_show_block), question, comment, required);

        $new_block.find(self.class_can_remove_field).val(can_remove);
        if (can_remove === '0'){
            $new_block.find(self.class_remove_button).hide();
            $new_block.find(self.class_edit_button).hide();
        }

        $new_block.show();
        $new_block.find(self.class_question_edit_block).hide();
        $new_block.find(self.class_notification_block).hide();

        return $new_block;
    }


    function add_question(){
        var $block = generate_question_block(0, '', '', '0', '1');
        edit_question($block);
        $block.find(self.class_actions_buttons_block).hide();
        self.$new_question_block.hide();
    }


    function send(data, $block, success, error){
        data.form_id = self.form_id;
        $.post(
            self.url,
            data,
            function(data){
                if (data.status === self.response_ok){
                    success(data);
                } else if (data.status === self.response_bad){
                    error(data);
                } else {
                    show_notification($block, self.response_bad, self.undefined_status);
                }
            }
        ).fail(function(){
            show_notification($block, self.response_bad, self.fail_message);
        });
    }


    function swap_visible($block_1, $block_2, _class){
        if (!$block_1.find(_class).is(":visible")){
            $block_2.find(_class).hide();
            $block_1.find(_class).show();
        }
    }


    function up_click($block){
        if (self.action_executed){
            return;
        }
        change_editable_block(null);
        var $prev_block = $block.prev();
        if ($prev_block.hasClass(self._class_question_block)){
            self.action_executed = true;
            send(
                {
                    question_id: $block.attr('id'),
                    action: self.up_action,
                    prev_question_id: $prev_block.attr('id')
                },
                $block,
                function(){
                    $block.insertBefore($prev_block);
                    swap_visible($prev_block, $block, self.class_up_button);
                    swap_visible($block, $prev_block, self.class_down_button);
                    self.action_executed = false;
                },
                function(data){
                    self.action_executed = false;
                    show_notification($block, data.status, data.message);
                }
            );
        } else {
            show_notification($block, self.response_bad, self.fail_up);
        }
    }


    function down_click($block){
        if (self.action_executed){
            return;
        }
        change_editable_block(null);
        var $next_block = $block.next();
        if ($next_block.hasClass(self._class_question_block)){
            self.action_executed = true;
            send(
                {
                    question_id: $block.attr('id'),
                    action: self.down_action,
                    next_question_id: $next_block.attr('id')
                },
                $block,
                function(){
                    $block.insertAfter($next_block);
                    swap_visible($next_block, $block, self.class_down_button);
                    swap_visible($block, $next_block, self.class_up_button);
                    self.action_executed = false;
                },
                function(data){
                    self.action_executed = false;
                    show_notification($block, data.status, data.message);
                }
            );
        } else {
            show_notification($block, self.response_bad, self.fail_down);
        }
    }


    function save_click($block){
        var $show_block = $block.find(self.class_question_show_block);
        var $edit_block = $block.find(self.class_question_edit_block);

        var question = $edit_block.find(self.class_question_field).val();
        var comment = $edit_block.find(self.class_comment_field).val();
        var is_required = $edit_block.find(self.class_required_field).is(':checked') ? "1" : "0";
        send(
            {
                question_id: $block.attr('id'),
                action: self.save_action,
                question: question,
                comment: comment,
                is_required: is_required
            },
            $block,
            function(data){
                set_values($show_block, question, comment, is_required);
                $show_block.show();
                $edit_block.hide();
                if (!parseInt($block.attr('id'))){
                    $block.attr('id', data.message.question_id);
                    $block.find(self.class_actions_buttons_block).show();
                    swap_visible($block.prev(), $block, self.class_down_button);
                    self.$new_question_block.show();
                }
                //show_notification(block, data.status, data.message.message);
            },
            function(data){
                show_notification($block, data.status, data.message);
            }
        );
    }


    function remove_click($block){
        if ($block.find(self.class_can_remove_field).val() === '0'){
            show_notification($block, self.response_bad, self.remove_required_field);
        } else {
            send(
                {
                    question_id: $block.attr('id'),
                    action: self.remove_action
                },
                $block,
                function(){
                    $block.remove();
                    self.$parent_block.find(self.class_question_block + ':first').find(self.class_up_button).hide();
                    self.$parent_block.find(self.class_question_block + ':last').find(self.class_down_button).hide();
                },
                function(data){
                    show_notification($block, data.status, data.message);
                }
            );
        }
    }


    function init() {
        self.$temp_block.hide();
        self.$parent_block.find(self.class_question_block + ':first').find(self.class_up_button).hide();
        self.$parent_block.find(self.class_question_block + ':last').find(self.class_down_button).hide();
        self.$parent_block.find(self.class_add_button).click(function () { add_question() });
    }


    this.generate_question_block = generate_question_block;
    this.init = init;
}
