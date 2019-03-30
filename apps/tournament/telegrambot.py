from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django_telegrambot.apps import DjangoTelegramBot
from . models import Motion, BotUsers, Language

import re
import logging

class TabmakerBot:

    __CALLBACK_NEXT_MOTION_ACTION = 'next_motion'
    __CALLBACK_CHANGE_LANGUAGE_ACTION = 'LANG_'

    def __init__(self, logger):
        self.logger = logger


    def motion_handler(self, bot, update):
        self.__send_motion(bot, update.message.chat_id, self.__get_or_create_user(update.message))


    def language_handler(self, bot, update):
        self.__get_or_create_user(update.message)

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
        user = self.__get_or_create_user(update.callback_query, update.callback_query.message.chat)
        lang_parser = re.match(
            self.__CALLBACK_CHANGE_LANGUAGE_ACTION + '(?P<lang_id>[0-9]+)',
            update.callback_query.data
        )

        if lang_parser:
            try:
                user.language = Language.objects.get(id=int(lang_parser.group('lang_id')))
                user.save()
                bot.sendMessage(
                    update.callback_query.message.chat_id,
                    text=(user.language.telegram_bot_label if user.language.telegram_bot_label else user.language.name),
                    # reply_markup=get_keyboard()
                )
            except Exception as e:
                self.logger.error(e)
                pass
        # elif update.callback_query.data == self.__CALLBACK_NEXT_MOTION_ACTION:

        return self.__send_motion(bot, update.callback_query.message.chat_id, user)


    def error_handler(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))


    def __get_or_create_user(self, message, chat=None):
        chat = chat or message.chat

        try:
            user, created = BotUsers.objects.get_or_create(
                user_id=message.from_user.id,
                username=message.from_user.username or '',
                first_name=message.from_user.first_name or '',
                last_name=message.from_user.last_name or '',
                chat_id=chat.id or 0,
                chat_name=chat.title or '',
            )
        except Exception as e:
            user = None
            self.logger.error(e)

        return user


    def __send_motion(self, bot, chat_id, user):
        motions = Motion.objects.filter(is_public=True)

        if user.language:
            motions = motions.filter(language=user.language)

        motion = motions.order_by('?').first()

        self.logger.info('{} // {} | {} | {}'.format(user, motion.id, motion.motion, motion.infoslide))

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


def main():
    logger = logging.getLogger('TelegramBot')
    logger.debug('Loading handlers for telegram bot')

    telegram_bot = TabmakerBot(logger)
    dp = DjangoTelegramBot.dispatcher
    dp.add_handler(CommandHandler('start', telegram_bot.language_handler))
    dp.add_handler(CommandHandler('language', telegram_bot.language_handler))
    dp.add_handler(CommandHandler('motion', telegram_bot.motion_handler))
    dp.add_handler(CallbackQueryHandler(telegram_bot.callback_query_handler))
    dp.add_error_handler(telegram_bot.error_handler)
