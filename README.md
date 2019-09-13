# Weather query Chatbot
## Demo<br>
![Demo](https://github.com/qiujw23/Chatbot/blob/master/chatbot_demo.gif "Demo")<br>  
## Configuration Instructions
## Installation Instructions
There are few online packages need to be installed for this project
### Rasa-NLU
***Prerequisites***<br>
<br>
Make sure your other packages on your computer are compatible with rasa-NLU.
***Setting up Rasa NLU***<br>
<br>
**Stable (Recommended)**<br>
The recommended way to install Rasa NLU is using pip which will install the latest stable version of Rasa NLU:<br>
```
$ pip install rasa_nlu
```
**Latest (Most recent github)**<br>
If you want to use the bleeding edge version you can get it from github:<br>
```
$ git clone https://github.com/RasaHQ/rasa_nlu.git
$ cd rasa_nlu
$ pip install -r requirements.txt
$ pip install -e .
```
Rasa NLU has different components for recognizing intents and entities, most of these will have some additional dependencies.<br>
When you train your model, Rasa NLU will check if all required dependencies are installed and tell you if any are missing.<br>  

***For more installation information***<br>
Go to https://rasa.com/docs/nlu/installation/<br>

### Telgram bot
***requirement***<br>
you just need to download telegram on its official website:https://telegram.org/apps and register and log in.
After that, search Bot_Father to achieve your own bot!
<br>

### pyTelegramBotAPI
***Setting up pyTelegramBotAPI***<br>
**From PyPI with pip (latest stable release):**<br>
```
$ pip install pyTelegramBotAPI
```
**From development repository (dev version):**<br>
Installation from source (requires git):<br>
```
$ git clone https://github.com/eternnoir/pyTelegramBotAPI.git
$ cd pyTelegramBotAPI
$ python setup.py install
```
***For more information***<br>
Go to https://github.com/eternnoir/pyTelegramBotAPI<br>
<br>
### The api I used
Go to https://rapidapi.com/community/api/open-weather-map?endpoint=53aa6041e4b00287471a2b62
and https://rapidapi.com/community/api/open-weather-map?endpoint=53aa6043e4b00287471a2b66
for more details
<br>
## operating instructions
1. Download all files in a same folder.
2. config_spacy.yml is the configuration file for rasa_NLU. demo-rasa.json is the file for rasa trainning.
3. Open `weather_bot.py` file in any IDE, the IDE I used to run is [Pycharm](https://www.jetbrains.com/pycharm/).
4. Change the statement below to chat with your own robot, you only need a token for telegram bot
    ```
    TOKEN = YOUR_TOKEN
    bot = telebot.TeleBot(TOKEN)
    ```
5. Run it, and just send message to your telegram bot. Then it will return information about weather or just chatting with you happliy.
6. Start to chat!
## contact information for the distributor or programmer
***Email:*** qiujw@shanghaitech.edu.cn<br>
***Website:*** https://github.com/qiujw23/mygit1
## a changelog
* 2019.9.11 uploade file 
* 2019.9.11 upload report, README.md
