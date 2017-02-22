from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from .models import Motion, BotUsers

import logging
logger = logging.getLogger('TelegramBot')


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def motion(bot, update):
    m = Motion.objects.filter(is_public=True).order_by('?').first()
    message = m.motion
    try:
        user, created = BotUsers.objects.get_or_create(
            user_id=update.message.from_user.id,
            username=update.message.from_user.username,
            first_name=update.message.from_user.first_name,
            last_name=update.message.from_user.last_name,
            chat_id=update.message.chat_id,
            chat_name=update.message.chat.title,
        )
        logger.info(str(user) + ' // ' + message + ' | ' + m.infoslide)
    except Exception as e:
        logger.error(e)

    if m.infoslide:
        message += '\n' + '\n' + m.infoslide

    bot.sendMessage(update.message.chat_id, text=message)


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.debug("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.TELEGRAM_BOT_TOKENS)
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("motion", motion))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], echo))

    # log all errors
    dp.add_error_handler(error)

    # log all errors
    dp.addErrorHandler(error)
