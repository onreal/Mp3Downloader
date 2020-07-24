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
bot_father = Blueprint('bot_father', __name__)

bot = telebot.TeleBot(config.Config.TELEGRAM_BOT)


@bot.message_handler(regexp="youtube.com|youtu.be")
def conversion_mode(message):
    process_db_transaction(message)

    if "youtu.be" in message.text:
        message.text.replace("youtu.be", "youtube.com")

    try:
        bot.send_message(message.chat.id, "Request received, conversion may take a while")
        # make the conversion
        filename = ConversionHelper(message.text).process_conversion()
        bot.send_message(message.chat.id, "File converted, sending now ...")

        # save file on directory
        directory = basedir + '/downloads/'
        filename = filename + '.mp3'

        # send as attachment
        audio = open(directory + filename, 'rb')
        bot.send_audio(message.chat.id, audio)

        # bot receive message
        # bot.reply_to(message, "Take your mp3 son ^^^")

        # remove mp3 from folder
        os.remove(directory + filename)

    except ReadTimeoutError as rte:
        print(rte)
        bot.reply_to(message, "This took to long son, retry with something else")
    except ConnectTimeoutError as cte:
        print(cte)
        bot.reply_to(message, "This took to long son, retry with something else")
    except ConnectTimeout as ct:
        bot.reply_to(message, "This took to long son, retry with something else")
        print(ct)
    except MaxRetryError as mre:
        bot.reply_to(message, "I tried many times to make things work for you without success, retry son")
        print(mre)
    except ConnectionError as ce:
        bot.reply_to(message, "I tried many times to make things work for you without success, retry son")
        print(ce)
    except ProtocolError as pe:
        bot.reply_to(message, "I tried many times to make things work for you without success, retry son")
        print(pe)
    except RegexNotFoundError as pe:
        bot.reply_to(message, "This couldn't work, something weired is happening with youtube, or not. Retry with another song! ")
        print(pe)
    except ApiException as ae:
        print(ae)
        bot.send_message(message.chat.id, "Telegram don't let me to upload files more than 50mb. Choose something "
                                          "smaller son")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "I tried many times to make things work for you without success, retry son")


@bot.message_handler(commands=['start'])
def new_comers(message):
    process_db_transaction(message)
    bot.send_message(message.chat.id, "Hello " + message.chat.first_name)
    bot.send_message(message.chat.id,
                     "I'm an mp3 finder & converter, my mission is clear, to search and or convert music for you... ")
    bot.send_message(message.chat.id,
                     "Currently my only search source is youtube and I only support mp3 conversion at 192Kbps")
    bot.send_message(message.chat.id,
                     "Telegram doesn't allow me to upload files more than 50mb, so results that occurs to more than 50mb have been filtered out")
    # bot.send_message(message.chat.id, "For requests say 'Listen to me bot' and after that your request")
    bot.send_message(message.chat.id,
                     "You can search inline by calling the @EasyMp3Bot or write to me and every word you say I will search for music. If any result found click on '/giveYTID' command.")
    bot.send_message(message.chat.id, "In case that you already have a youtube url just provide it to me and I will respond back with the mp3 file")
    bot.send_message(message.chat.id, "Inpatient tip1: Conversion may take a while, i'll let you know once is ready")
    bot.send_message(message.chat.id,
                     "Inpatient tip2: If you blame on me or use bad words, no problem, I always respond with music")
    bot.send_message(message.chat.id,
                     "If you want to view this message again type /start or /help for a short version")
    bot.send_message(message.chat.id, "HOT and Recommended is to search inline with @EasyMp3Bot")


@bot.message_handler(commands=['help', 'yo'])
def new_comers(message):
    bot.send_message(message.chat.id,
                     "For start message /start, to search inline @EasyMp3Bot")


@bot.message_handler(func=lambda message: True)
def search_mode(message):
    #socket.emit('roufa_minima', message.text, broadcast=True)
    bot.send_message(message.chat.id, "...")
    process_db_transaction(message)
    if '/give' not in message.text:
        yt_results = YtSearch(message.text, message.from_user.language_code).perform_search()
        if len(yt_results) <= 0:
            bot.send_message(message.chat.id, "Nothing found son, try again something else")
            return
        count = 0
        for res_dict in yt_results:
            duration = int("".join(filter(str.isdigit, res_dict['vid_duration'])))
            if duration < 3800:
                count += 1
                search_res = res_dict['vid_title'] + res_dict['vid_duration'] + ' /give' + res_dict['vid_id']
                bot.send_message(message.chat.id, search_res)
                time.sleep(0.3)
            else:
                continue
        else:
            bot.send_message(message.chat.id, "Hey son, I found " + count.__str__() + " results")
    else:
        the_id = message.text.partition("/give")[2]
        if the_id == 'YTID':
            bot.send_message(message.chat.id, "This is just an example. Try give from results")
        else:
            message.text = 'https://www.youtube.com/watch?v=' + the_id
            conversion_mode(message)


@bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
def test_chosen(chosen_inline_result):
    result = chosen_inline_result
    pass


# @bot.inline_handler(lambda query: query.query == 'want')
# def query_text(inline_query):
#     try:
#         # yt_results = YtSearch(message.text, message.from_user.language_code).perform_search()
#         # if len(yt_results) <= 0:
#         #     bot.send_message(message.chat.id, "Nothing found son, try again something else")
#         #     return
#         #
#         # for res_dict in yt_results:
#         #     search_res = res_dict['vid_title'] + res_dict['vid_duration'] + ' /give' + res_dict['vid_id']
#         #     bot.send_message(message.chat.id, search_res)
#         #     time.sleep(0.5)
#         # else:
#         #     bot.send_message(message.chat.id, "Hey son, I found " + len(yt_results).__str__() + " results")
#         inlinequery = inline_query
#         r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
#         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
#         bot.answer_inline_query(inline_query.id, [r, r2])
#     except Exception as e:
#         print(e)


@bot.inline_handler(lambda query: len(query.query) >= 2)
def search_inline(inline_query):
    results_push = list()
    try:
        yt_results = YtSearch(inline_query.query, inline_query.from_user.language_code).perform_search()
        if len(yt_results) <= 0:
            results_push.append(
                types.InlineQueryResultArticle("Nothing found son, try again something else").reply_markup)
        else:
            for idx, res_dict in enumerate(yt_results):
                duration = int("".join(filter(str.isdigit, res_dict['vid_duration'])))
                if duration < 3800:
                    results_push.append(types.InlineQueryResultArticle(
                        thumb_url=res_dict['vid_thumbnail'],
                        description='ytid:' + res_dict['vid_id'] + ' ' + res_dict['vid_duration'],
                        title=res_dict['vid_title'], id=idx,
                        input_message_content=types.InputTextMessageContent(message_text='/give' + res_dict['vid_id'])))
        bot.answer_inline_query(inline_query.id, results_push)
    except Exception as e:
        print(e)


def bot_logger(message, user):
    try:
        with app.app_context():
            BotLogger(botpersonid=user.id, request=message.text, success=False).insert()
            return BotLogger.query.filter_by(botpersonid=user.id).first()
    except RuntimeError as re:
        print(re)
        return False


def bot_person(message):
    try:
        with app.app_context():

            # check if user exists
            user = BotPerson.query.filter_by(socialId=str(message.from_user.id)).first()
            # if user doesnt exists insert

            if not user:
                person = {
                    "name": message.from_user.first_name,
                    "surname": message.from_user.last_name,
                    "username": message.from_user.username,
                    "socialId": str(message.from_user.id),
                    "platform": "telegram",
                    "chatid": message.chat.id
                }

                BotPerson(person).insert()
            elif user.chatid != message.chat.id:
                user.chatid = message.chat.id
                user.commit()

            return BotPerson.query.filter_by(socialId=str(message.from_user.id)).first()

    except RuntimeError as re:
        print(re)
        return False


def process_db_transaction(message):
    user = bot_person(message)
    logger = bot_logger(message, user)
    if not logger or not user:
        bot.reply_to(message, "Something weired happened")


bot.polling(none_stop=True, timeout=600)
