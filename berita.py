import requests
from telegram.ext import ConversationHandler

import json
from urllib.request import Request, urlopen
from urllib.parse import quote_plus

error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

# =======================================
# List of predefined Function
def get_berita_from_query(query_string):
    """Get News List from Query"""
    detect_berita_in_word = query_string.find("berita")
    # If berita isn't found on text, we set the int to 0 otherwise it's 7
    if detect_berita_in_word == -1:
        index_string = 0
    else:
        index_string = detect_berita_in_word + 7
    query_url = quote_plus(query_string[index_string:])

    url = "http://news.developeridn.com/search/?q="+query_url
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        get_body = json.loads(webpage)

        # List out berita before sending them to user
        list_berita = ['*{0}. {1}*{2}\n{3}'.format(i+1,
                                                  el.get('judul'),
                                                  el.get('waktu'),
                                                  el.get('link'))
                        for i, el in enumerate(get_body.get('data'))]

        # Check if we got any news from the API
        if get_body['length'] > 0:
            response = ("*Ini daftar berita terkini tentang "
                        + query_string[index_string:]
                        + " yaa...* 😁\n\n")
            response += "\n".join(list_berita)
        else:
            response = "Aku gak nemuin berita yang kamu cari. Maaf ya 😢"
        return response
    except:
        return error_server_resp

# =========================================

def get_news(update, context):
    """Send news to user that is using keyword to search news"""
    query_string = update.message.text.lower()
    response = get_berita_from_query(query_string)
    update.message.reply_text(response, parse_mode='Markdown')
    update.message.reply_text(end_chat)
    return ConversationHandler.END