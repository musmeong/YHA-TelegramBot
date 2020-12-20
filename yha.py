import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, ConversationHandler
import os
import json

# Get function from every bot features defined in other files
from wiki import *
from berita import *
from corona import *
from visual import *
from motion import *
from hearing import *

FIRST, SECOND = range(2)

with open("token.json",) as f:
    TOKEN = json.load(f)
    f.close()

# Create folder to store temporary files, if it doesnt exist
if not os.path.exists('tmp'):
    os.makedirs('tmp')

# Enable logging
logging.basicConfig(format=('%(asctime)s - %(name)s - '
                            '%(levelname)s - %(message)s'),
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    first_name = update.message.chat['first_name']
    last_name = update.message.chat['last_name']
    if last_name:
        name = first_name + " " + last_name
    else:
        name = first_name

    response = ("Halo, " + name + "! 🙋‍♂️\n\n"
    
                "Kenalin, aku YHA! Your Health Assistant~\n"
                "Di sini aku bakal sediain info kesehatan yang berguna untuk "
                "kamu. Kamu bisa mulai dengan klik command di bawah.\n\n"

                "*1. /infocorona*\n"
                "Untuk mendapatkan informasi terbaru Corona di Indonesia "
                "yang diupdate daily.\n\n"

                "*2. /infodetailcorona*\n"
                "Untuk mendapatkan informasi terbaru Corona di provinsi "
                "yang kamu pilih yang diupdate daily.\n\n"

                "*3. /infopolusi*\n"
                "Untuk mendapatkan informasi terkini polusi "
                "udara di sekitar kamu.\n\n"

                "*4. /infonutrisi*\n"
                "Untuk mendapatkan informasi nutrisi dari "
                "makanan yang kamu foto.\n\n"

                "*5. /deteksibatuk*\n"
                "Untuk mendeteksi jenis batukmu berdasarkan rekaman suara "
                "batukmu. Hmm, meskipun aku masih perlu banyak belajar buat "
                "ini sih. Cuman, aku punya kejutan kalo misal aku gabisa "
                "nebak jenis batukmu.\n\n"

                "*6. /deteksimood*\n"
                "Kamu tau kan kalo mood itu juga berpengaruh ke kesehatan. "
                "Yuk coba ngomong ke aku pake voice note, aku coba tebak "
                "mood kamu saat ini apa.\n\n"

                "*7. Cari tahu topik kesehatan* atau */pengentahu*\n"
                "Tulis pertanyaan mulai dengan keyword \"apa itu\" atau "
                "\"siapa itu\" (case insensitive). Contohnya: "
                "\"apa itu cacar?\". Kamu juga bisa klik command /pengentahu "
                "lalu masukin keyword yang mau kamu cari yaa.\n\n"

                "*8. Cari tahu berita* atau */cariberita*\n"
                "Aku bakal kasih berita-berita terkini secara real time dari "
                "CNN tiap kali kamu tulis chat apapun dimulai dengan \"berita\""
                "(case insensitive). Contohnya: \"berita vaksin\". Kamu juga "
                "bisa klik command /cariberita lalu masukin keyword "
                "yang mau kamu cari yaa.\n\n"

                "Klik aja menu di atas buat mulai yaaa~\n\n"

                "Semua layanan yang ada di bot ini didukung oleh "
                "pihak ketiga yang bisa kamu temuin di command /lisensi.")
    update.message.reply_text(response, parse_mode='Markdown')


def bantuan(update, context):
    """Autoresponse if user sends command /bantuan"""
    response = ("/start - mulai bot\n"
                "/bantuan - lihat daftar command\n"
                "/infocorona - tracking kasus corona\n"
                "/infodetailcorona - kasus corona per provinsi\n"
                "/infopolusi - ketahui polusi di sekitarmu\n"
                "/infonutrisi - menebak nutrisi dari foto makanan\n"
                "/deteksibatuk - deteksi batuk dari suara\n"
                "/deteksimood - tebak mood dari suara\n"
                "/pengentahu - cari tahu sesuatu\n"
                "/cariberita - cari berita terkini realtime\n"
                "/lisensi - lisensi yg digunakan bot ini\n")
    update.message.reply_text(response)


def lisensi(update, context):
    """Autoresponse to show third-party license when user sends /lisensi"""
    response = ("*Berikut layanan pihak ketiga yang digunakan untuk "
                "mendukung penggunaan dari bot ini:*\n\n"

                "*1. Info Corona*\n"
                "Diperoleh dari pemerintah Indonesia "
                "(https://data.covid19.go.id/) dan diupdate harian.\n\n"

                "*2. Info Polusi*\n"
                "Diperoleh dengan API dari WAQI (https://waqi.info/).\n\n"

                "*3. Info Nutrisi*\n"
                "Gambar diproses menggunakan Visual Recogition dari IBM "
                "Watson. Gambar yang sudah diproses dan menghasilkan makanan "
                "yang ditebak selanjutnya diimport ke Edamam "
                "(https://developer.edamam.com/) untuk mendapatkan "
                "detail kandungan nutrisinya.\n\n"

                "*4. Deteksi Batuk*\n"
                "Suara yang dikirim user akan diproses dalam CoughTracker dari "
                "RapidAPI (https://rapidapi.com/CoughTracker/api/coughapi/)\n\n"

                "*5. Deteksi Mood*\n"
                "Suara yang dikirim user akan diproses dan dikonversi menjadi "
                "file WAV menggunakan service dari CloudConvert API "
                "(https://cloudconvert.com/api/v2). Suara yang dikonversi "
                "selanjutnya diproses lewat API ke Empath "
                "(https://webempath.net/).\n\n"

                "*6. Ensiklopedia*\n"
                "Keyword diproses menggunakan library Wikipedia di Python "
                "(https://pypi.org/project/wikipedia/) yang mana menggunakan "
                "MediaWiki untuk mengambil data dari Wikipedia.\n\n"

                "*7. Berita Terkini*\n"
                "Data diambil menggunakan API dari CNN Indonesia "
                "(https://www.news.developeridn.com/).\n\n")
    update.message.reply_text(response, parse_mode='Markdown')


def ask_keyword(update, context):
    """Autoresponse if user using chat to trigger ensiklopedia or berita"""
    response = "Masukin keyword yang mau kamu cari ya 🕵️‍♂️..."
    update.message.reply_text(response)
    return FIRST


def batal(update, context):
    """To cancel the conversation if user sends command /batal"""
    response = "Oke, kita batalkan."
    update.message.reply_text(response)
    return ConversationHandler.END


def info_polusi_response(update, context):
    """Autoresponse if user sends command command /infopolusi."""
    response = ("Langsung share lokasi kamu berada sekarang ya. "
                "Tapi harus pake Telegram di HP kamu ya. "
                "Lalu caranya tinggal klik attachment trus share location. "
                "Aku bakal bantu analisis data polusi "
                "di sekitar kamu secara real time!")
    update.message.reply_text(response)


def info_nutrisi_response(update, context):
    """Autoresponse if user sends command /infonutrisi."""
    response = ("Tiap kali kamu upload foto makanan ke aku, "
                "aku akan ngasih tahu beberapa detail nutrisi yang ada "
                "di makanan itu. Jadi kamu gak perlu khawatir kalau mau "
                "makan ini itu selama ada aku~")
    update.message.reply_text(response)


def bot_not_understand(update, context):
    """Autoresponse if bot doesn't understand the text or command from user."""
    response = ("Maaf. Aku ga paham maksud kamu apa 😢. "
                "Kalau misal bingung, pakai command /bantuan "
                "atau /start yaa.")
    update.message.reply_text(response)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN['TELEGRAM_BOT_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bantuan", bantuan))
    dp.add_handler(CommandHandler("lisensi", lisensi))
    dp.add_handler(CommandHandler("infocorona", info_corona_umum))
    dp.add_handler(CommandHandler("infopolusi", info_polusi_response))
    dp.add_handler(CommandHandler("infonutrisi", info_nutrisi_response))
    
    # Handle Command for Wikipedia using Command
    conversation_corona_handler = ConversationHandler(
        entry_points=[CommandHandler("infodetailcorona", ask_choice_covidprov)],
        states={
            FIRST: [MessageHandler(Filters.text, info_corona_provinsi)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(conversation_corona_handler)

    # Handle Command for Cough Check using Command
    conversation_cough_handler = ConversationHandler(
        entry_points=[CommandHandler("deteksibatuk", detect_batuk_response)],
        states={
            FIRST: [MessageHandler(Filters.text, force_to_reply_cough),
                    MessageHandler(Filters.voice, cough_check)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(conversation_cough_handler)

    # Handle Command for Mood Check using Command
    convmood_handler = ConversationHandler(
        entry_points=[CommandHandler("deteksimood", detect_mood_response)],
        states={
            FIRST: [MessageHandler(Filters.text, force_to_reply_mood),
                    MessageHandler(Filters.voice, mood_check)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(convmood_handler)

    # Handle Command for Wikipedia using Command
    convwikicom_handler = ConversationHandler(
        entry_points=[CommandHandler("pengentahu", ask_keyword)],
        states={
            FIRST: [MessageHandler(Filters.text, get_topic)],
            SECOND: [MessageHandler(Filters.text, get_summary)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(convwikicom_handler)

    # Handle if News use Command
    convnews_handler = ConversationHandler(
        entry_points=[CommandHandler("cariberita", ask_keyword)],
        states={
            FIRST: [MessageHandler(Filters.text, get_news)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(convnews_handler)

    # on noncommand i.e message
    dp.add_handler(MessageHandler(Filters.regex('(?i)^berita'), get_news))
    dp.add_handler(MessageHandler(Filters.photo, process_photo))
    dp.add_handler(MessageHandler(Filters.location, process_location))
    dp.add_handler(MessageHandler(Filters.voice, voice_note_response))
    
    # Handle Command for Wikipedia using Keyword
    regex_wiki = '(?i)^(?:si)?apa itu'
    convwiki_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(regex_wiki), get_topic)],
        states={
            SECOND: [MessageHandler(Filters.text, get_summary)]
        },
        fallbacks=[CommandHandler("batal", batal)]
    )
    dp.add_handler(convwiki_handler)

    dp.add_handler(MessageHandler(Filters.text, bot_not_understand))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()