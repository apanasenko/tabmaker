from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django_telegrambot.apps import DjangoTelegramBot
from .models import Motion, BotUsers, Language

import re
import logging
logger = logging.getLogger('TelegramBot')


def register_user(message, chat=None):
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
        logger.error(e)

    return user


def motion(bot, update):
    send_motion(bot, update.message.chat_id, register_user(update.message))


def send_motion(bot, chat_id, user):
    logger.debug(chat_id)
    logger.debug(user)
    motions = Motion.objects.filter(is_public=True)

    if user.language:
        motions = motions.filter(language=user.language)

    motion = motions.order_by('?').first()

    logger.info('{} // {} | {} | {}'.format(user, motion.id, motion.motion, motion.infoslide))

    message = motion.motion
    if motion.infoslide:
        message += '\n' + '\n' + motion.infoslide

    bot.sendMessage(chat_id, text=message, reply_markup=get_keyboard())


def lang(bot, update):
    register_user(update.message)

    def get_lang_button(lang: Language) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            lang.telegram_bot_label if lang.telegram_bot_label else lang.name,
            callback_data=('LANG_%d' % lang.id)
        )

    bot.sendMessage(
        update.message.chat_id,
        text='Choose language:',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [get_lang_button(lang) for lang in Language.objects.filter(is_public=True)]
            ],

        )
    )

def callback_query(bot, update):
    user = register_user(update.callback_query, update.callback_query.message.chat)
    lang_parser = re.match('LANG_(?P<lang_id>[0-9]+)', update.callback_query.data)
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
            logger.error(e)
            pass
    # elif update.callback_query.data == 'next_motion':

    return send_motion(bot, update.callback_query.message.chat_id, user)


def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Next motion', callback_data='next_motion')],
    ])


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.debug("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", lang))
    dp.add_handler(CommandHandler("lang", lang))

    dp.add_handler(CommandHandler("motion", motion))
    dp.add_handler(CallbackQueryHandler(callback_query))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
