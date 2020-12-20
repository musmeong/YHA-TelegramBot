from telegram.ext import ConversationHandler
import wikipedia

import warnings
warnings.filterwarnings('ignore')

wikipedia.set_lang("id")
FIRST, SECOND = range(2)

error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

# =======================================
# List of predefined Function
def get_wiki_title_from_query(query_string):
    """Get Wikipedia page title from query."""
    global get_title
    
    detect_itu_in_word = query_string.find("itu")
    # If keyword isn't found on text, we set the int to 0 otherwise it's 3
    if detect_itu_in_word == -1:
        index_string = 0
    else:
        index_string = detect_itu_in_word + 4
    
    try:
        get_title = wikipedia.search(query_string[index_string:])
        response = "*Silakan pilih topik yang mau kamu tau:*\n"
        response += "\n".join(["/{0} {1}".format(i+1, el)
                               for i, el in enumerate(get_title)])
    except:
        response = error_server_resp
    
    return response
    
# =========================================

def get_topic(update, context):
    """Send Wiki title list to user for searching further in wiki."""
    query_string = update.message.text.lower()
    response = get_wiki_title_from_query(query_string)
    update.message.reply_text(response, parse_mode='Markdown')
    return SECOND

def get_summary(update, context):
    """Send Wiki summary from the title that is chosen by user."""
    query = update.message.text

    # Check if user send command to choose page or not by detect the number
    try:
        number = int(query[1:])
    except:
        if query != "/batal":
            response = ("Kamu harus pilih angka yang ada, "
                        "atau klik /batal jika ingin batal.")
            update.message.reply_text(response)
            return SECOND
        else:
            response = "Oke, kita batalkan."
            update.message.reply_text(batal)
            return ConversationHandler.END

    # Try to get summary of Wikipedia page that is chosen
    try:
        res_wiki = wikipedia.summary(get_title[number-1])

        # Split Output if message length more than 4096 (max Tele chat = 4096)
        if len(res_wiki) > 4096:
            for x in range(0, len(res_wiki), 4096):
                update.message.reply_text(res_wiki[x:x+4096],
                                            parse_mode='Markdown')
        else:
            update.message.reply_text(res_wiki, parse_mode='Markdown')
        update.message.reply_text(end_chat)
        return ConversationHandler.END
    except:
        response = ("Laman tersebut error nih waktu ditarik. Maaf ya.\nIni "
                    "karena ada beberapa page di Wikipedia yang punya keyword "
                    "yang sama kayak yang lagi kamu cari (ambiguasi).\n\n"
                    "Bisa coba cari keyword lebih detail yaa. 😢")
        update.message.reply_text(response)
        return ConversationHandler.END