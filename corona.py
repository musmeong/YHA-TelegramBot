import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import requests
import os
import pandas as pd
from telegram.ext import ConversationHandler

# Define dot thousand separator
trans = str.maketrans('.,', ',.')

FIRST, SECOND = range(2)

# Set the image size and properties for the chart
sns.set(rc={'figure.figsize': (15,7),
            'axes.facecolor': 'white',
            'figure.facecolor': 'white',
            'ytick.labelsize': '15'})
colors = ['orange', 'red', 'blue', 'green']
customPalette = sns.set_palette(sns.color_palette(colors))

temp_string = 'tmp/'

error_server_resp = "Maaf sedang ada gangguan di server saat ini... 😢"
end_chat = "Interaksi selesai. Klik /bantuan buat liat daftar command lain. 😄"

def parse_response_covid(*args, **kwargs):
    """Parse JSON into list of response to user"""
    if args:
        response = "*" + args[0] + "*:\n"
    else:
        response = ""

    for key, value in kwargs.items():
        response += "*" + key + ':* {:,}'.format(value).translate(trans) + "\n"
    response += "\n"

    return response

def make_plot(data, filename):
    """Make data into line plot"""
    ax = sns.lineplot(data=data, palette=customPalette, linewidth=3.5)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
    ylabels = ['{:,.0f}'.format(x/1000) + 'K'
                if x > 10000 else '{:,.0f}'.format(x)
                for x in ax.get_yticks()]
    ax.set_yticklabels(ylabels)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(prop={'size': 16})
    ax.figure.savefig(filename)
    plt.close()

def info_corona_umum(update, context):
    """Response after user sends /infocorona. Bot will give info about Covid."""
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    url_corona = "https://data.covid19.go.id/public/api/update.json"
    try:
        data_corona = requests.request("GET", url_corona).json()
        data_harian = data_corona['update']['harian']
        data_update = data_harian[-1]
        
        response = ("Data terakhir diupdate pada *"
                    + data_corona['update']['penambahan']['created'] + "*\n\n")
        response += parse_response_covid(
                        "Penambahan terbaru",
                        Sembuh=data_update['jumlah_sembuh']['value'],
                        Dirawat=data_update['jumlah_dirawat']['value'],
                        Positif=data_update['jumlah_positif']['value'],
                        Meninggal=data_update['jumlah_meninggal']['value'])
        response += parse_response_covid(
                        "Jumlah Kumulatif",
                        Sembuh=data_update['jumlah_sembuh_kum']['value'],
                        Dirawat=data_update['jumlah_dirawat_kum']['value'],
                        Positif=data_update['jumlah_positif_kum']['value'],
                        Meninggal=data_update['jumlah_meninggal_kum']['value'])
        response += parse_response_covid(
                        "Data Lain-lain",
                        **{"Orang Dalam Pemantauan":
                                data_corona['data']['jumlah_odp'],
                            "Pasien Dalam Pengawasan":
                                data_corona['data']['jumlah_pdp'],
                            "Total Spesimen":
                                data_corona['data']['total_spesimen'],
                            "Total Spesimen Negatif":
                                data_corona['data']['total_spesimen_negatif']})
        response += ("Untuk memperoleh detail kasus per provinsi, "
                     "kamu bisa pakai command /infodetailcorona yaa.")
        update.message.reply_text(response, parse_mode = 'Markdown')

        x = [el['key_as_string'][:10] for el in data_harian]
        jdk = [el['jumlah_dirawat_kum']['value'] for el in data_harian]
        jmk = [el['jumlah_meninggal_kum']['value'] for el in data_harian]
        jpk = [el['jumlah_positif_kum']['value'] for el in data_harian]
        jsk = [el['jumlah_sembuh_kum']['value'] for el in data_harian]
        jm = [el['jumlah_meninggal']['value'] for el in data_harian]
        js = [el['jumlah_sembuh']['value'] for el in data_harian]
        jp = [el['jumlah_positif']['value'] for el in data_harian]
        data = pd.DataFrame({"Date": x,
                            "Jumlah Dirawat Kumulatif": jdk,
                            "Jumlah Meninggal Kumulatif": jmk,
                            "Jumlah Positif Kumulatif": jpk,
                            "Jumlah Sembuh Kumulatif": jsk})
        data = data.set_index("Date")

        chart_all = temp_string + str(msg_id) + '_all.png'
        make_plot(data, chart_all)
        context.bot.sendPhoto(chat_id=chat_id, photo=open(chart_all, 'rb'))

        data = pd.DataFrame({"Date": x,
                            "Jumlah Kasus Positif": jp})
        data = data.set_index("Date")
        data['Rata-Rata Kasus 7 hari Terakhir'] = data.rolling(window=7).mean()

        chart_pos = temp_string + str(msg_id) + '_pos.png'
        make_plot(data, chart_pos)
        context.bot.sendPhoto(chat_id=chat_id, photo=open(chart_pos, 'rb'))
        
        update.message.reply_text(end_chat)
        os.remove(chart_all)
        os.remove(chart_pos)
    except:
        update.message.reply_text(error_server_resp)
    
def ask_choice_covidprov(update, context):
    """Response to give detailed information about Covid-19 per province."""
    global list_city
    global detail_corona
    url_detail_corona = "https://data.covid19.go.id/public/api/prov.json"
    try:
        detail_corona = requests.request("GET", url_detail_corona).json()
        data_update = detail_corona['last_date']

        response = ("Data terakhir kali diupdate di tanggal "
                    + data_update 
                    + " nih...\nMau pilih provinsi apa?\n")
        
        list_city = [el['key'].title() for el in detail_corona['list_data']]
        list_city_command = ['/{0} {1}'.format(i+1, el)
                             for i, el in enumerate(list_city)]
        response += '\n'.join(list_city_command)

        update.message.reply_text(response)
        return FIRST
    except:
        update.message.reply_text(error_server_resp)
        return ConversationHandler.END

def info_corona_provinsi(update, context):
    query = update.message.text
    try:
        number = int(query[1:]) 
        pilih = detail_corona['list_data'][number-1]

        response = ("*Data Detail Kasus Corona di "
                    + pilih['key'].title()
                    + "*\n\n")
        response += parse_response_covid(
                        **{"Jumlah Dirawat": pilih['jumlah_dirawat'],
                            "Jumlah Kasus": pilih['jumlah_kasus'],
                            "Jumlah Meninggal": pilih['jumlah_meninggal'],
                            "Jumlah Sembuh": pilih['jumlah_sembuh']})
        response += parse_response_covid(
                        "Penambahan Terakhir",
                        Meninggal=pilih['penambahan']['meninggal'],
                        Positif=pilih['penambahan']['positif'],
                        Sembuh=pilih['penambahan']['sembuh'])
        response += parse_response_covid(
                        "Jenis Kelamin Pasien",
                        **{"Pasien Laki-laki":
                                pilih['jenis_kelamin'][0]['doc_count'],
                            "Pasien Perempuan":
                                pilih['jenis_kelamin'][1]['doc_count']})
        response += "*Kelompok Umur Pasien*\n"
        list_umur = ["*"+el['key']+" tahun: *"+"{:,}"
                    .format(el['doc_count']).translate(trans)
                    for el in pilih['kelompok_umur']]
        response += '\n'.join(list_umur)

        update.message.reply_text(response, parse_mode='Markdown')
        update.message.reply_text(end_chat)
        return ConversationHandler.END
    except:
        if query != "/batal":
            response = ("Kamu harus pilih angka yang ada, "
                        "atau klik /batal jika ingin batal.")
            update.message.reply_text(response)
            return FIRST
        else:
            response = "Pencarian dibatalkan."
            update.message.reply_text(response)
            return ConversationHandler.END