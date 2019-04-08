from typing import Optional

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django_telegrambot.apps import DjangoTelegramBot
from . models import Motion, BotUsers, BotChat, Language, TelegramToken, User

import re
import logging
import datetime

class TabmakerBot:

    __CALLBACK_NEXT_MOTION_ACTION = 'next_motion'
    __CALLBACK_CHANGE_LANGUAGE_ACTION = 'LANG_'

    def __init__(self, logger):
        self.logger = logger


    def motion_handler(self, bot, update):
        user, chat = self.__get_or_create_user(update.message.from_user, update.message.chat)
        self.__send_motion(bot, update.message.chat_id, user, chat)


    def start_handler(self, bot, update):
        user, chat = self.__get_or_create_user(update.message.from_user, update.message.chat)

        token = update.message.text.split('/start')[1].strip()
        if token:
            connected_user = self.__connect_user(user, chat, token)
            bot.sendMessage(
                update.message.chat_id,
                text=('Канал привязан к пользователю %s' % connected_user.name()),
            )

        # TODO print help


    def language_handler(self, bot, update):
        self.__get_or_create_user(update.message.from_user, update.message.chat)

        bot.sendMessage(
            update.message.chat_id,
            text='Choose language:',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [self.__build_language_buttons(language) for language in Language.objects.filter(is_public=True)]
                ],
            )
        )


    def callback_query_handler(self, bot, update):
        user, chat = self.__get_or_create_user(update.callback_query.from_user, update.callback_query.message.chat)
        lang_parser = re.match(
            self.__CALLBACK_CHANGE_LANGUAGE_ACTION + '(?P<lang_id>[0-9]+)',
            update.callback_query.data
        )

        if lang_parser:
            try:
                language = Language.objects.get(id=int(lang_parser.group('lang_id')))
                if chat:
                    chat.language = language
                    chat.save()
                else:
                    user.language = language
                    user.save()

                bot.sendMessage(
                    update.callback_query.message.chat_id,
                    text=(language.telegram_bot_label if language.telegram_bot_label else language.name),
                    # reply_markup=get_keyboard()
                )
            except Exception as e:
                self.logger.error(e)
                pass
        # elif update.callback_query.data == self.__CALLBACK_NEXT_MOTION_ACTION:

        return self.__send_motion(bot, update.callback_query.message.chat_id, user, chat)


    def error_handler(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))


    def __get_or_create_user(self, from_user, from_chat):
        user = None
        chat = None

        try:
            user, created = BotUsers.objects.update_or_create(
                id=from_user.id,
                username=from_user.username or '',
                first_name=from_user.first_name or '',
                last_name=from_user.last_name or '',
            )

            if from_chat.id != from_user.id:
                chat, created = BotChat.objects.update_or_create(
                    id=from_chat.id,
                    title=from_chat.title,
                )

        except Exception as e:
            self.logger.error(e)

        return user, chat


    def __send_motion(self, bot, chat_id, user, chat):
        motions = Motion.objects.filter(is_public=True)

        language = chat.language if chat else user.language
        if language:
            motions = motions.filter(language=language)

        motion = motions.order_by('?').first()

        self.logger.info('{} {} // {} | {} | {}'.format(user, chat, motion.id, motion.motion, motion.infoslide))

        message = motion.motion
        if motion.infoslide:
            message += '\n' + '\n' + motion.infoslide

        bot.sendMessage(chat_id, text=message, reply_markup=self.__build_motion_keyboard())


    def __build_language_buttons(self, language: Language) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            language.telegram_bot_label if language.telegram_bot_label else language.name,
            callback_data=self.__CALLBACK_CHANGE_LANGUAGE_ACTION + str(language.id)
        )


    def __build_motion_keyboard(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Next motion', callback_data=self.__CALLBACK_NEXT_MOTION_ACTION)],
        ])


    def __connect_user(self, bot_user: BotUsers, chat: BotChat, token: str) -> Optional[User]:
        if chat is not None:
            self.logger.warning('')
            return None

        token: TelegramToken = TelegramToken.objects.filter(value=token).first()

        if token is None:
            self.logger.warning('')
            return None

        if token.expire < datetime.datetime.now():
            raise Exception('Время жизни токена закончилось, попробуйте заново')

        token.user.telegram = bot_user
        token.user.save()

        return token.user


def main():
    logger = logging.getLogger('TelegramBot')
    logger.debug('Loading handlers for telegram bot')

    telegram_bot = TabmakerBot(logger)
    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(CommandHandler('start', telegram_bot.start_handler))
    dp.add_handler(CommandHandler('language', telegram_bot.language_handler))
    dp.add_handler(CommandHandler('motion', telegram_bot.motion_handler))
    dp.add_handler(CallbackQueryHandler(telegram_bot.callback_query_handler))
    dp.add_error_handler(telegram_bot.error_handler)
