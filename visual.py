from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import json

with open("token.json",) as f:
    TOKEN = json.load(f)
    f.close()

# Define dot thousand separator
trans = str.maketrans('.,', ',.')

error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

def parse_response_edamam(data, **kwargs):
    """Parse JSON into list of response (nutrition from Edamam) to user"""
    response = ""
    nutrition = requests.request("GET", TOKEN['EDAMAM_URL'] + data).json()
    for key, value in kwargs.items():
        try:
            nutrient = nutrition['totalNutrients']
            daily_need = nutrition['totalDaily']
            response += ("\t*{0}: {1:,.1f} {2}*\n"
                        "\t(memenuhi *{3:,.1f}{4}* kebutuhan harian)\n"
                        .format(key,
                                nutrient[value]['quantity'],
                                nutrient[value]['unit'],
                                daily_need[value]['quantity'],
                                daily_need[value]['unit'])
                        .translate(trans))
        except:
            pass

    return response

# Authenticate Visual Recognition
authenticator = IAMAuthenticator(TOKEN['IBM_VR_TOKEN'])
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator)
visual_recognition.set_service_url(TOKEN['IBM_VR_URL']) 

def process_photo(update, context):
    """Process photo that is sent from user and detect object in the photo"""
    # Get last photo that is sent
    file = context.bot.get_file(update.message.photo[-1].file_id)
    file_path = context.bot.get_file(file).file_path

    update.message.reply_text("Memproses gambar 👨‍🎨...")
    update.message.reply_text("Sabar yaaa. Mungkin bisa agak lama 🙄...")

    try:
        classes = visual_recognition.classify(url=file_path,
                                            threshold='0.6',
                                            classifier_ids='food').get_result()
        object_labeled = classes['images'][0]['classifiers'][0]['classes']

        # Check if object is food or not, then give response
        if object_labeled[0]['class'] != 'non-food':
            res = ["*{0}. {1} (aku yakin {2:,}%)*\n\n{3}\n"
                    .format(i+1,
                            el['class'].title(),
                            el['score']*100,
                            parse_response_edamam(el['class'],
                                                Kalori="ENERC_KCAL",
                                                Protein="PROCNT",
                                                Lemak="FAT",
                                                Karbo="CHOCDF"))
                    for i, el in enumerate(object_labeled)]
            response = "\n".join(res)
        
            update.message.reply_text(response, parse_mode='Markdown')
            update.message.reply_text(end_chat)
        else:
            response = ("Hmm... Sepertinya aku gabisa nebak ini makanan apa, "
                        "atau gambar yang kamu upload bukan makanan. 😓")
            update.message.reply_text(response)
    except:
        update.message.reply_text(error_server_resp)