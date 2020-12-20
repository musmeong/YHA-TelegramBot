import cloudconvert
from scipy.io import wavfile
import requests
from telegram.ext import ConversationHandler
import os
import json

with open("token.json",) as f:
    TOKEN = json.load(f)
    f.close()

FIRST, SECOND = range(2)
error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

def voice_note_response(update, context):
    """Autoresponse when user sends voice note message"""
    response = ("Haloo 🙋‍♂️\n"
                "Aku liat kamu baru ngirim file suara. Aku bisa loh nebak "
                "sesuatu dari kamu pake suaramu. Pake command di bawah ya. "
                "Tapi kamu harus rekam lagi hehe 🎤\n"
                "1. /deteksibatuk\n"
                "2. /deteksimood")
    update.message.reply_text(response)

def detect_batuk_response(update, context):
    """Autoresponse when user sends /deteksibatuk command"""
    response = ("Kamu boleh upload suara rekaman batuk kamu ke aku sekarang. "
                "Kalo mau lanjut, aku bisa tau jenis batukmu apa juga. "
                "Langsung rekam dari HP aja ya~ 🎤\n"
                "Kalau mau batal, pake command /batal yaa.")
    update.message.reply_text(response)
    return FIRST

def detect_mood_response(update, context):
    """Autoresponse when user sends /deteksimood command"""
    response = ("Kamu boleh upload rekaman suara kamu ngomong ke aku sekarang. "
                "Ntar aku coba tebak moodmu saat ini apa, hehe. "
                "Langsung rekam dari HP aja ya~ 🎤\n"
                "Kalau mau batal, pake command /batal yaa.")
    update.message.reply_text(response)
    return FIRST

def force_to_reply_cough(update, context):
    """Autoresponse when user doesn't send voice note after /deteksibatuk"""
    if update.message.text.lower() != "/batal":
        response = ("Ayo rekam suara batukmu 🎤. "
                    "Kalo misal gajadi, bisa pake command /batal yaa...")
        update.message.reply_text(response)
        return FIRST
    else:
        response = "Oke, kita batalkan."
        update.message.reply_text(response)
        return ConversationHandler.END

def force_to_reply_mood(update, context):
    """Autoresponse when user doesn't send voice after /deteksimood"""
    if update.message.text.lower() != "/batal":
        response = ("Ayo rekam suara kamu 🎤. "
                    "Kalo misal gajadi, bisa pake command /batal yaa...")
        update.message.reply_text(response)
        return FIRST
    else:
        response = "Oke, kita batalkan."
        update.message.reply_text(response)
        return ConversationHandler.END

def cough_check(update, context):
    """Detect cough from voice note that is sent by user"""
    response = "Memproses suara batukmu 👨🏼‍💻..."
    update.message.reply_text(response)

    file = context.bot.get_file(update.message.voice.file_id)
    
    url_coughcheck = "https://coughapi.p.rapidapi.com/v1/recognize/url"
    file_path = context.bot.get_file(file).file_path

    payload = "{\r\"url\": \"" + file_path + "\"\r}"
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': TOKEN['COUGHTRACKER_TOKEN'],
        'x-rapidapi-host': "coughapi.p.rapidapi.com"
    }
    try:
        # Detect Cough
        res = requests.request("POST", url_coughcheck,
                                    data=payload, headers=headers)
        res = res.json()['result']['episodes']
        cough_list = [("{0}. Batuk jenis {1} di detik {2} "
                       "sampai {3} dengan {4}% dahak.")
                       .format(i+1,
                              "kering" if el['coughType']=="dry" else "basah",
                              el['start'],
                              el['end'],
                              round(el['wetPrediction']*100))
                        for i, el in enumerate(res)]
        response = "\n".join(cough_list)
        if len(response) == 0:
            response = ("Aku gak bisa deteksi batuknya di rekaman tadi 🙇🏼‍♂️. "
                        "Kamu mungkin bisa coba agak jauhin suaramu "
                        "dari mikrofon. Maaf 😢")
        
        update.message.reply_text(response)
        update.message.reply_text(end_chat)
        return ConversationHandler.END
    except:
        update.message.reply_text(error_server_resp)
        return ConversationHandler.END

def mood_check(update, context):
    """Detect mood from voice note that is sent by user"""
    response = "Kamu punya suara keren. Aku analisis dulu ya... 👨🏿‍💻"
    update.message.reply_text(response)

    file = context.bot.get_file(update.message.voice.file_id)
    file_path = context.bot.get_file(file).file_path
    # Get some parts of the File ID to name audio file
    file_id = context.bot.get_file(file).file_id[-7:]

    url_empath = 'https://api.webempath.net/v2/analyzeWav'
    apikey_empath = TOKEN['EMPATH_TOKEN']
    payload = {'apikey': apikey_empath}
    apikey_cloudconvert = TOKEN['CLOUDCONVERT_TOKEN']
    
    try:
        # Convert OGA from Telegram Voice Note to WAV using CloudConvert
        cloudconvert.configure(api_key = apikey_cloudconvert)
        history_convert = cloudconvert.Job.create(payload={
            "tasks": {
                'import-my-file': {
                    'operation': 'import/url',
                    'url': file_path
                },
                'convert-my-file': {
                    'operation': 'convert',
                    'input': 'import-my-file',
                    'output_format': 'wav'
                },
                'export-my-file': {
                    'operation': 'export/url',
                    'input': 'convert-my-file'
                }
            }
        })
        exported_url_task_id = history_convert['tasks'][-1]['id']
        res = cloudconvert.Task.wait(id=exported_url_task_id)
        file = res.get("result").get("files")[0]
        
        response = "🎵 Mengkonversi file audio ke data... 🎵"
        update.message.reply_text(response)
        
        filename = "tmp/{}.wav".format(file_id)
        res = cloudconvert.download(filename=filename, url=file['url'])
        
        _, audio_file = wavfile.read(filename)
        # Get only first 5 seconds and 11025 sample rate to use API
        wavfile.write(filename, 11025, audio_file[0:5000])
        data = open(filename, 'rb')
        audio_file = {'wav': data}

        response = "Sebentar lagi! 🔎 Sedang melakukan analisis mendalam... 🔎"
        update.message.reply_text(response)
        
        # Detect Mood
        res_audio = requests.post(url_empath,
                                 params=payload,
                                 files=audio_file).json()
        data.close()
        os.remove(filename)

        if res_audio['error'] == 0:
            response = "*Ini hasil analisisku yaa. Maaf kalo sotoy, hehe..*\n"
            result_parse = {"Kalem": "calm",
                            "Marah": "anger",
                            "Bahagia": "joy",
                            "Sedih": "sorrow",
                            "Energik": "energy"}
            for key, value in result_parse.items():
                response += "*{0} :* {1}%\n".format(key, res_audio[value]*2)

            update.message.reply_text(response, parse_mode='Markdown')
            update.message.reply_text(end_chat)
        else:
            response = ("Maaf 😢 Ada kesalahan waktu proses suara kamu. "
                        "Kamu bisa coba lagi abis ini yaa.")
            update.message.reply_text(response)
        return ConversationHandler.END
    except:
        update.message.reply_text(error_server_resp)
        return ConversationHandler.END