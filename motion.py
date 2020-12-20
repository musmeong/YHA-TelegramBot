import requests
from datetime import datetime, timedelta
import json

with open("token.json",) as f:
    TOKEN = json.load(f)
    f.close()

# Define dot thousand separator
trans = str.maketrans('.,', ',.')

error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

# Get Today Date
today_date = (datetime.today() + timedelta(hours=7)).strftime("%Y-%m-%d")

def parse_response_waqi(data, title, **kwargs):
    """Parse JSON into list of response to user"""
    response = "*" + title + "*\n"
    
    for key, value in kwargs.items():
        try:
            score = data[value]['v']
            response += "*{0}:* {1:,}\n".format(key, score).translate(trans)
        except:
            pass
    response += "\n"

    return response

def parse_response_forecast_waqi(data, title, **kwargs):
    """Parse JSON into list of response (polution forecast) to user"""
    response = title + "\n\n\n"
    for key, value in kwargs.items():
        try:
            response += "*" + key + ":*\n\n"
            
            response += "Rata-rata\n"
            list_forecast = ["Tanggal {0}: {1}".format(el['day'], el['avg'])
                            for el in data[value]
                            if el['day']>=today_date]
            response += "\n".join(list_forecast)
            response += "\n\n"
            
            response += "Range (Jangkauan Nilai)\n"
            list_forecast = ["Tanggal {0}: {1} – {2}"
                                .format(el['day'], el['min'], el['max'])
                                for el in data[value]
                                if el['day']>=today_date]
            response += "\n".join(list_forecast)
            response += "\n\n\n"
        except:
            pass

    return response

def process_location(update, context):
    """Process latlong that is sent from user and get polution data"""
    lat = update.message.location.latitude
    lng = update.message.location.longitude

    url_waqi = (f"https://api.waqi.info/feed/geo:{lat};{lng}/?token="
                + TOKEN['WAQI_TOKEN'])
    try :
        polution = requests.get(url_waqi).json()
        if polution['status'] == "ok":
            polution_data = polution['data']
            polution_iaqi = polution_data['iaqi']
            response = ("Kamu sedang berada di *"
                        + polution_data['city']['name']
                        + "* dengan Air Quality Index *"
                        + str(polution_data['aqi'])
                        + "*")

            response_detail = parse_response_waqi(
                                polution_iaqi,
                                ("Ini detail untuk polusi udara "
                                "di sekitar kamu..."),
                                **{"Karbon Monoksida": 'co',
                                    "Kelembapan Relatif": 'h',
                                    "Nitrogen Dioksida": 'no2',
                                    "Ozone": 'o3',
                                    "Tekanan Atmosfer": 'p',
                                    "Partikulat PM2,5": 'pm25',
                                    "Partikulat PM10": 'pm10',
                                    "Belerang Dioksida": 'so2',
                                    "Temperatur": 't',
                                    "Angin": 'w'})

            response_forecast = parse_response_forecast_waqi(
                                    polution['data']['forecast']['daily'],
                                    ("Nah ini forecast beberapa indeks polusi "
                                    "untuk beberapa hari ke depan..."),
                                    **{"Ozone": "o3",
                                    "Partikulat PM2,5": "pm25",
                                    "Partikulat PM10": "pm10",
                                    "Radiasi Ultraviolet": "uvi"})

            update.message.reply_text(response, parse_mode='Markdown')
            update.message.reply_text(response_detail, parse_mode='Markdown')
            update.message.reply_text(response_forecast, parse_mode='Markdown')
        else:
            update.message.reply_text(error_server_resp)
    except :
        update.message.reply_text(error_server_resp)
    