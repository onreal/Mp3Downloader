import time

import telebot
from youtube_dl.utils import RegexNotFoundError

from flask import Blueprint
from requests.exceptions import ConnectTimeout, ConnectionError
from requests.packages.urllib3.exceptions import ReadTimeoutError, ConnectTimeoutError, MaxRetryError, ProtocolError
from telebot import types
from telebot.apihelper import ApiException

from app import os, basedir, config, create_app
from app.helpers.YtSearch import YtSearch
from app.helpers.ConversionHelper import ConversionHelper
from app.model.pgsql.BotPerson import BotPerson
from app.model.pgsql.BotLogger import BotLogger

app = create_app()
app.app_context().push()
bot_broadcast = Blueprint('bot_broadcast', __name__)

bot = telebot.TeleBot(config.Config.TELEGRAM_BOT)

users = BotPerson.query.filter(BotPerson.socialId is not None)

# TODO normal here is to use the chatId
# TODO take messages from table
for user in users:
    try:
        bot.send_message(user.socialId, "Hey " + user.name + ", mp3 father is full functional again, hooray!")
        time.sleep(2)
        bot.send_message(user.socialId, "I dare you to share songs directly from Youtube App to Telegram -> Mp3Father, "
                                        "you will be amazed! @EasyMp3Bot <- for inline search")
        time.sleep(2)
        bot.send_message(user.socialId, "Song Titles are now full shown in Greek and English language, but best of "
                                        "all ...")
        time.sleep(1)
        bot.send_message(user.socialId, "Song conversion rate upgraded at 256kbp/s!")
        time.sleep(1)
        bot.send_message(user.socialId, "Your music father Salut you <3")
    except Exception as e:
        continue

bot.polling(none_stop=True, timeout=600)
