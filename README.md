<p align="center">
<img src="https://i.ibb.co/bND3r4t/photo-2020-12-16-00-57-13.jpg" width="128" height="128"/>
</p>
<p align="center">
<a href="#"><img title="Telegram-Bot" src="https://img.shields.io/badge/Telegram Bot-blue?colorA=%23ff0000&colorB=%230088cc&style=for-the-badge"></a>
</p>
<p align="center">
<a href="https://github.com/musmeong"><img title="Author" src="https://img.shields.io/badge/AUTHOR-MusMeong-blue.svg?style=for-the-badge&logo=github"></a>
</p>

## Getting Started

This project require Python3.6+



### Install

Clone this project

```bash
> git clone https://github.com/musmeong/YHA-TelegramBot.git
> cd YHA-TelegramBot
```

Install the dependencies:

```bash
> pip install -r requirements.txt 
```

Get API for the features. Look further on [API Section](https://github.com/musmeong/YHA-TelegramBot#API) on how to get each of them. Then change the token key in JSON file.



### Usage

Run the Telegram bot

```bash
> python yha.py
```



### API

- Get Telegram Bot API Key by following steps from [this website](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token) and change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L1).

  **Info Polusi**

- Get WAQI API Key by signing up on [this website](https://aqicn.org/data-platform/token/#/) and change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L3). (**Note:** Free User get 1000 requests per second)

  **Info Nutrisi**

- Get IBM Visual Recognition API and URL by following steps from [this website](https://cloud.ibm.com/docs/visual-recognition?topic=visual-recognition-getting-started-tutorial) to detect object in the photo. Change the token on [this section for API](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L6) and [this section for URL](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L7). (**Warning**: VisualRecognition IBM will be deprecated on 1 December 2021)

- Get Edamam API by signing up on [this website](https://developer.edamam.com/edamam-nutrition-api) and change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L8). (**Note:** Free User get 1000 requests per month)

  **Deteksi Batuk**

- Get CoughTracker API from [this website](https://rapidapi.com/CoughTracker/api/coughapi), the key is on the "X-RapidAPI-Key" label. Change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L5).

  **Deteksi Mood**

- Get CloudConvert API Key to convert OGA Telegram Audio to WAV by signing up on [this website](https://cloudconvert.com/dashboard/api/v2/keys) and change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L4). (**Note:** Free User get 25 minutes conversion per day)

- Get Empath API Key by signing up on [this website](https://webempath.net/agreement) and change the token on [this section](https://github.com/musmeong/YHA-TelegramBot/blob/main/token.json#L2). (**Note:** Free User get 250-300 requests per month)



### Deployment

This repository already have [Aptfile](https://github.com/musmeong/YHA-TelegramBot/blob/main/Procfile), [Procfile](https://github.com/musmeong/YHA-TelegramBot/blob/main/Procfile), and [runtime.txt](https://github.com/musmeong/YHA-TelegramBot/blob/main/runtime.txt) that is left default using Python3.7 to be deployed on Heroku. You can deploy the bot using another option, but I recommend use [Heroku](heroku.com).

1. Login with your existing account or Sign Up if you don't have one.

2. After getting into the dashboard, Click on the "New" button on upper right and choose "Create New App".

3. Give your app a name and click "Create App".

4. Follow the instruction on "Deploy using Heroku Git" section.

   

---

## Features and How To Trigger

| Features                                 | Command / Trigger                                            | Third-Party Used                                             |
| ---------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Corona Information and All-time Chart    | /infocorona                                                  | [Gugus Tugas Covid-19]()                                     |
| Corona Information Details per Province  | /infodetailcorona                                            | [Gugus Tugas Covid-19]()                                     |
| Polution Information near User Location  | /infopolusi                                                  | [World Air Quality Index](https://waqi.info/)                |
| Nutrition Information from Food in Photo | /infonutrisi                                                 | [IBM Watson](https://www.ibm.com/id-en/cloud/watson-visual-recognition)<br />[Edamam](edamam.com) |
| Cough Detect from Voice Note             | /deteksibatuk                                                | [CoughTracker](https://rapidapi.com/CoughTracker/api/coughapi) |
| Mood Detect from Voice Note              | /deteksimood                                                 | [Empath](https://webempath.net/)                             |
| Encyclopedia                             | /pengentahu (or using "apa itu" or "siapa itu"<br />in the beginning of chat) | [Wikipedia](https://pypi.org/project/wikipedia/)             |
| Real-time News                           | /cariberita (or using "berita" <br />in the beginning of chat) | [DeveloperIDN](http://developeridn.com/)                     |



## To-Do

 - IBM Watson Assistant Integration.
 - Change the appearance of the command (using InlineKeyboard on Telegram).
 - Using self-made models to reduce API usage and add more features.
 - Using Speech to Text or Text to Speech to utilize visually impaired user.



## Documentation

[https://drive.google.com/file/d/1zHJ8lFpDqeCZL-1iz2AqRKgVZcAwhXNS/preview](https://drive.google.com/file/d/1zHJ8lFpDqeCZL-1iz2AqRKgVZcAwhXNS/preview)



---

## Thanks to

- [FarizDotID](https://github.com/farizdotid/DAFTAR-API-LOKAL-INDONESIA)