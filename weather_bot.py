# -*- coding: utf-8 -*-
# Import necessary modules
import telebot
from telebot import types
import re
import random
import datetime
import requests


from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config


patterns = {'greet': re.compile("hello|hi |hey |what's up |Hello|Hi|Hey|What's up|How are you"),
		    'goodbye': re.compile('bye|farewell|goodbye|byebye|End|Stop|Bye|Farewell|Goodbye|Byebye|end|stop'),
		    'deny': re.compile(" no | not | never |n't|No |Never"),
		    'affirm': re.compile(' yes | yep | sure | alright | Yes | Yep | Sure | Alright ')}

TOKEN = '848155393:AAG6B13DllTeO8PeG3aWkJ4ujVQJ7IL1I2I'

bot = telebot.TeleBot(TOKEN)


today = datetime.date.today().strftime("%Y-%m-%d")

class replyKeyboard():
    def startKeyboard():
        markup_start = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('/start')
        markup_start.add(itembtn1)
    def helpKeyboard():
        markup_help = types.ReplyKeyboardMarkup(row_width=2)
        itembtn2 = types.KeyboardButton('/help')
        markup_help.add(itembtn2)

#get start
@bot.message_handler(commands=['start'])
def bot_start(message):
    if message.text == '/start':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'Hello, I am bot DavidQ. :) \n'
                                          'I can chat with you as a friend. You can say whatever you want to me!  (￣ˇ￣) \n'
                                          'More importantly! I can give you some information about the weather of the cities you want to know about. ~\n'
                                          'If you what more information about my command, just tell me /help. (￣ε(￣)' , reply_markup=replyKeyboard.startKeyboard())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'Sorry my dear friend. I am not sure if you what to start chatting with me. :(\n'
                                          'Please enter /start to chat with me! ', reply_markup=replyKeyboard.startKeyboard())

#want get some help
@bot.message_handler(commands=['help'])
def bot_help(message):
    if message.text == '/help':
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'I can chat with you with some simple sentence.\n'
                                          'You can also ask some questions about the weather! But remember to tell me which city you want to know first.  ^_^ \n'
                                          'Not only can I give you information about the weather today, but also I am able to show you some details about the weather forecast for the next ten days. []~(￣▽￣)~*\n'
                                          'Besides the temperature, I have many other specific information to provide for you, such humidity, pressure... \n',
                                          'If you doesn\'t tell me city or date, I will set city to Shanghai and date to today as defaults. \n'
                                          'Am I powerful? <(￣︶￣)>　Can\'t wait to start talking to me? Let\'s get it!',reply_markup=replyKeyboard.startKeyboard())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,
                         'Sorry my dear friend. I am not sure if you what to get some help and know more details about the functions of mine. ?_?\n'
                         'Please enter /help to get help! ^_^', reply_markup=replyKeyboard.helpKeyboard())


name = "DavidQ"

# Define a dictionary containing a list of ask_name for each message
ask_name = {
  "what's your name?": [
      "my name is {0}".format(name),
      "they call me {0}".format(name),
      "I go by {0}".format(name),
      "you can call me {0}".format(name)
   ],
   "Can you tell me your name?": [
      "my name is {0}".format(name),
      "they call me {0}".format(name),
      "I go by {0}".format(name),
      "you can call me {0}".format(name)
   ],
}

rules = {'I would like to (.*)': ['What would it mean if you got {0}',
                         'Why do you want {0}',
                         "What's stopping you from getting {0}"],
         'do you remember (.*)': ['Did you think I would forget {0}',
                                  "Why haven't you been able to forget {0}",
                                  'What about {0}',
                                  'Yes .. and?'],
         'do you think (.*)': ['if {0}? Absolutely.',
                               'No chance',
                               'of course! I always think {0}'],
         'if (.*)': ["Do you really think it's likely that {0}",
                     'Do you wish that {0}',
                     'What do you think about {0}',
                     'Really--if {0}']
        }

say_hello = {
	"with_name": ["What's up! {0}",
				  "Welcome to the new world! {0}",
				  "I am happy to chat with you, dear {0}",
				  "Hello, {0}!",
				  "Hi, {0}! Please enjoy yourself here!"],
	"no_name":["I am interested in being your friend",
			   "Welcome come to chat with me!",
			   "Hello my friend! My name is DavidQ",
			   "Nice to meet you!",
			   "How are you!"]
}

say_goodbye = {'bye':["Alright, byebye!",
                      "Goodbye my friend!",
                      "See you next time!",
                      "Bye!"]}

def match_rule(rules, message):
    for pattern, responses in rules.items():
        match = re.search(pattern, message)
        if match is not None:
            response = random.choice(responses)
            var = match.group(1) if '{0}' in response else None #group(0),group(1)
            return response, var
    return 'default', None

def replace_pronouns(message):
    message = message.lower()
    if 'me ' in message:
        return re.sub('me', 'you', message)
    if 'i ' in message:
        return re.sub('i', 'you', message)
    elif 'my ' in message:
        return re.sub('my', 'your', message)
    elif 'your ' in message:
        return re.sub('your', 'my', message)
    elif 'you ' in message:
        return re.sub('you', 'me', message)

    return message

def respond_rules(message):
    # Call match_rule
    response, phrase = match_rule(rules, message)
    if response != 'default':
        if '{0}' in response:
            # Replace the pronouns in the phrase
            phrase = replace_pronouns(phrase)
            # Include the phrase in the response
            response = response.format(phrase)
        return response
    else:
        return message

def rasa_train(message):
    training_data = load_data('demo-rasa.json')
    # Create a trainer
    trainer = Trainer(config.load("config_spacy.yml"))
    # Create an interpreter by training the model
    interpreter = trainer.train(training_data)
    response = interpreter.parse(message)
    matched_intent = None
    for intent, pattern in patterns.items():
        if re.search(pattern,message) is not None:
            matched_intent = intent
            response["intent"]["name"] = matched_intent
    return response

def find_name(message):
    name = None
    # Create a pattern for checking if the keywords(name and call) occur
    name_keyword = re.compile('name|call')
    # Create a pattern for finding capitalized words
    name_pattern = re.compile('[A-Z]{1}[a-z]+')
    if name_keyword.search(message):
        # Get the matching words in the string
        name_words = name_pattern.findall(message)
        if len(name_words) > 0:
            # Return the name if the keywords are present
            name = ' '.join(name_words)  #many words in a list change to a str
            sent_head = "Hello|Hi|Hey|What's|How|Why|What|Who|My"
            if re.search(sent_head,name) is not None:
                delete = re.findall(sent_head,name).pop()+' '
                name = re.sub(delete,'',name)
    return name

def current_weather(message,city = "Shanghai", weather = None):
    global real_weather
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"callback": "test", "id": "2172797", "units": "\"metric\" or \"imperial\"", "mode": "xml, html","q": "Shanghai"}
    try:
        querystring['q'] = str(city)

        headers = {
			'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
			'x-rapidapi-key': "925d2685d3msha9d08e5660f54e7p129f08jsn9d1ee9a65b48"
			}

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_text = response.text
        #print(response_text)
        r_t_del1 = re.sub('test'+'\(','',response_text)
        r_t_del2 = re.sub('\)','',r_t_del1)
        response_dict = eval(r_t_del2)
        #print(response_dict)

        main_weather = response_dict['weather'][0]['main']
        weather_description = response_dict['weather'][0]['description']
        #print(weather_description)
        temp = round(response_dict['main']['temp'] - 273, 2)
        press = response_dict['main']['pressure']
        humi = response_dict['main']['humidity']
        temp_min = round(response_dict['main']['temp_min'] - 273, 2)
        temp_max = round(response_dict['main']['temp_max'] - 273, 2)
        visi = response_dict['visibility']
        wind_spe = response_dict['wind']['speed']
        #wind_deg = response_dict['wind']['deg']
        #print(temp,press,humi,temp_min,temp_max,visi,wind_spe,wind_deg)

        if main_weather == 'Clouds':
            real_weather = 'cloudy'
        elif main_weather == 'Rain':
            real_weather = 'rainy'
        elif main_weather == 'Clear':
            real_weather = 'sunny'

        reply0 = 'Today, the weather is mainly {0}'.format(real_weather) + '\n'
        reply00 = '{0} outside!'.format(weather_description) + '\n'
        reply1 = 'Now, the temperature is {0} degrees Celsius'.format(temp) + ' (￣ˇ￣)\n'
        reply2 = 'The maximal temperature will be {0} degrees Celsius'.format(temp_max) + ' <(￣︶￣)>\n'
        reply3 = 'In the mean while, the minimal temperature will be {0} degrees Celsius'.format(temp_min) + ' []~(￣▽￣)~*\n'
        reply4 = 'What\'s more,the pressure of the air is {0} Pa'.format(press) + ' (￣▽￣)~*\n'
        reply5 = 'And the humidity of the air is {0}%'.format(humi) + ' (=￣ω￣=)\n'
        reply6 = 'At the same time, the visibility today is  {0}'.format(visi) + ' (￣３￣)a\n'
        reply7 = 'The wind speed is {0} mps'.format(wind_spe) + ' (￣0 ￣)y\n'
        #reply8 = 'The wind degree is {0} degrees'.format(wind_deg) + '>o<\n'

        if temp >= 30:
            reply9 = 'Today is so hot! ~_~ It is a good idea to eat some ice-cream!' + '\n'
        elif temp >= 10 and temp < 30:
            reply9 = 'The temperature today is very mild! ^_^ You can go for a walk or go out for fun!' + '\n'
        else:
            reply9 = 'Today is so cold! T_T Remember to wear enough clothes!' + '\n'

        if wind_spe <= 5:
            reply10 = 'There\'s little wind outside! The wind is very mild!' + '\n'
        elif wind_spe > 5 and wind_spe<= 10:
            reply10 = 'It\'s a little windy outside but not too strong! The wind is very mild!' + '\n'
        else:
            reply10 = 'The wind outside is so strong! Please be careful when you go out' + '\n'

        bot.send_message(message.chat.id,reply0+reply00)

        if weather == 'hot' or weather == 'cold' or weather == 'mid':
            bot.send_message(message.chat.id,reply1+reply2+reply3+reply9)
        elif weather == 'windy':
            bot.send_message(message.chat.id,reply7+reply10)
        elif weather == 'cloudy':
            if real_weather == 'Clouds':
                reply11 = 'It\'s clouy outside.' + '\n'
            else:
                reply11 = 'It\'s not clouy outside.' + '\n'
            bot.send_message(message.chat.id,reply11+reply6)
        elif weather == 'rain':
            if real_weather == 'rainy':
                reply12 = 'It\'s rainy outside. Please remember to bring an umbrella with you when going out!' + '\n'
            else:
                reply12 = 'It\'s not rainy outside! You can just go outside without taking an umbrella.' + '\n'
            bot.send_message(message.chat.id,reply12+reply5)
        else:
            bot.send_message(message.chat.id,reply1+reply2+reply3+reply4+reply5+reply6+reply7)
    except KeyError:
        bot.send_message(message.chat.id,'Sorry, it seems that you did tell me a correct city name. Please try again!  T_T')


def forecast_weather(message,city = "Shanghai", date = 1, weather = None):
    global real_weather_morn, real_weather_noon, real_weather_night
    url = "https://community-open-weather-map.p.rapidapi.com/forecast"

    querystring = {"q": "Shanghai"}
    querystring["q"] = city
    new_day = (datetime.datetime.today()+datetime.timedelta(days=date)).strftime("%Y-%m-%d")

    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "925d2685d3msha9d08e5660f54e7p129f08jsn9d1ee9a65b48"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_text = response.text
    r_t_del1 = re.sub('test'+'\(','',response_text)
    r_t_del2 = re.sub('\)','',r_t_del1)
    response_dict = eval(r_t_del2)
    #print(response_dict)

    that_day = []
    morning = '09:00:00'
    afternoon = '15:00:00'
    evening = '18:00:00'
    try:
        for i in range(0,40):
            dt_txt = response_dict['list'][i]['dt_txt']
            a = re.search(new_day+' (.*)',dt_txt)
            if a is not None:
                if a.group(1) == morning or a.group(1) == afternoon or a.group(1) == evening:
                    that_day.append(response_dict['list'][i])


        temp_morn = round(that_day[0]['main']['temp'] - 273, 2)
        temp_min_morn = round(that_day[0]['main']['temp_min'] - 273, 2)
        temp_max_morn = round(that_day[0]['main']['temp_max'] - 273, 2)
        humi_morn = that_day[0]['main']['humidity']
        main_weather_morn = that_day[0]['weather'][0]['main']
        weather_description_morn = that_day[0]['weather'][0]['description']
        wind_spe_morn = that_day[0]['wind']['speed']
        wind_deg_morn = that_day[0]['wind']['deg']

        if main_weather_morn == 'Clouds':
            real_weather_morn = 'cloudy'
        elif main_weather_morn == 'Rain':
            real_weather_morn = 'rainy'
        elif main_weather_morn == 'Clear':
            real_weather_morn = 'sunny'

        bot.send_message(message.chat.id,'In the morning:')
        reply0_m = 'The main weather is {0}'.format(real_weather_morn) + '\n'
        reply00_m = '{0} outside!'.format(weather_description_morn) + '\n'
        reply1_m = 'The temperature is {0} degrees Celsius'.format(temp_morn) + '>o<\n'
        reply2_m = 'The maximal temperature will be {0} degrees Celsius'.format(temp_max_morn) + ' (￣ˇ￣)\n'
        reply3_m = 'In the mean while, the minimal temperature will be {0} degrees Celsius'.format(temp_min_morn) + ' (￣0 ￣)y\n'
        reply4_m = 'And the humidity of the air is {0}%'.format(humi_morn) + ' (=￣ω￣=)\n'
        reply5_m = 'The wind speed is {0} mps'.format(wind_spe_morn) + ' []~(￣▽￣)~*\n'
        reply6_m = 'The wind degree is {0} degrees'.format(wind_deg_morn) + '<(￣︶￣)> \n'
        bot.send_message(message.chat.id,reply0_m+reply00_m+reply1_m+reply2_m+reply3_m+reply4_m+reply5_m+reply6_m)


        temp_noon = round(that_day[1]['main']['temp'] - 273, 2)
        temp_min_noon = round(that_day[1]['main']['temp_min'] - 273, 2)
        temp_max_noon = round(that_day[1]['main']['temp_max'] - 273, 2)
        humi_noon = that_day[1]['main']['humidity']
        main_weather_noon = that_day[1]['weather'][0]['main']
        weather_description_noon = that_day[1]['weather'][0]['description']
        wind_spe_noon = that_day[1]['wind']['speed']
        wind_deg_noon = that_day[1]['wind']['deg']

        if main_weather_noon == 'Clouds':
            real_weather_noon = 'cloudy'
        elif main_weather_noon == 'Rain':
            real_weather_noon = 'rainy'
        elif main_weather_noon == 'Clear':
            real_weather_noon = 'sunny'

        bot.send_message(message.chat.id,'In the afternoon:')
        reply0_no = 'The main weather is {0}'.format(real_weather_noon) + '\n'
        reply00_no = '{0} outside!'.format(weather_description_noon) + '\n'
        reply1_no = 'The temperature is {0} degrees Celsius'.format(temp_noon) + ' (>_<)\n'
        reply2_no = 'The maximal temperature will be {0} degrees Celsius'.format(temp_max_noon) + ' (￣< ￣)\n'
        reply3_no = 'In the mean while, the minimal temperature will be {0} degrees Celsius'.format(temp_min_noon) + ' (+o+)\n'
        reply4_no = 'And the humidity of the air is {0}%'.format(humi_noon) + ' (^_-)\n'
        reply5_no = 'The wind speed is {0} mps'.format(wind_spe_noon) + ' (￣0 ￣)y\n'
        reply6_no = 'The wind degree is {0} degrees'.format(wind_deg_noon) + '(^。^)\n'
        bot.send_message(message.chat.id,reply0_no+reply00_no+reply1_no+reply2_no+reply3_no+reply4_no+reply5_no+reply6_no)

        temp_night = round(that_day[2]['main']['temp'] - 273, 2)
        temp_min_night = round(that_day[2]['main']['temp_min'] - 273, 2)
        temp_max_night = round(that_day[2]['main']['temp_max'] - 273, 2)
        humi_night = that_day[2]['main']['humidity']
        main_weather_night = that_day[2]['weather'][0]['main']
        weather_description_night = that_day[2]['weather'][0]['description']
        wind_spe_night = that_day[2]['wind']['speed']
        wind_deg_night = that_day[2]['wind']['deg']

        if main_weather_night == 'Clouds':
            real_weather_night = 'cloudy'
        elif main_weather_night == 'Rain':
            real_weather_night = 'rainy'
        elif main_weather_night == 'Clear':
            real_weather_night = 'sunny'

        bot.send_message(message.chat.id,'In the evening:')
        reply0_ni = 'The main weather is {0}'.format(real_weather_night) + '\n'
        reply00_ni = '{0} outside!'.format(weather_description_night) + '\n'
        reply1_ni = 'The temperature is {0} degrees Celsius'.format(temp_night) + '  ( > v < )\n'
        reply2_ni = 'The maximal temperature will be {0} degrees Celsius'.format(temp_max_night) + ' (O ^ ~ ^ O)\n'
        reply3_ni = 'In the mean while, the minimal temperature will be {0} degrees Celsius'.format(temp_min_night) + ' (>_<)\n'
        reply4_ni = 'And the humidity of the air is {0}%'.format(humi_night) + ' ∩▽∩\n'
        reply5_ni = 'The wind speed is {0} mps'.format(wind_spe_night) + ' Lo(￣▽￣///)\n'
        reply6_ni = 'The wind degree is {0} degrees'.format(wind_deg_night) + ' (～o￣v￣)～o ~\n'
        bot.send_message(message.chat.id,reply0_ni+reply00_ni+reply1_ni+reply2_ni+reply3_ni+reply4_ni+reply5_ni+reply6_ni)

        if temp_noon >= 30:
            reply9 = 'Today is so hot! ~_~ It is a good idea to eat some ice-cream!' + '\n'
        elif temp_noon >= 10 and temp_noon < 30:
            reply9 = 'The temperature today is very mild! ^_^ You can go for a walk or go out for fun!' + '\n'
        else:
            reply9 = 'Today is so cold! T_T Remember to wear enough clothes!' + '\n'

        if wind_spe_noon <= 5:
            reply10 = 'There\'s little wind outside! The wind is very mild!' + '\n'
        elif wind_spe_noon > 5 and wind_spe_noon <= 10:
            reply10 = 'It\'s a little windy outside but not too strong! The wind is very mild!' + '\n'
        else:
            reply10 = 'The wind outside is so strong! Please be careful when you go out' + '\n'


        if weather == 'hot' or weather == 'cold' or weather == 'mid':
            bot.send_message(message.chat.id,reply9)
        elif weather == 'windy':
            bot.send_message(message.chat.id,reply10)
        elif weather == 'cloudy':
            if real_weather_noon == 'Clouds':
                reply11 = 'It\'s clouy outside.' + '\n'
            else:
                reply11 = 'It\'s not clouy outside.' + '\n'
            bot.send_message(message.chat.id,reply11)
        elif weather == 'rain':
            if real_weather_noon == 'rainy':
                reply12 = 'It\'s rainy outside. Please remember to bring an umbrella with you when going out!' + '\n'
            else:
                reply12 = 'It\'s not rainy outside! You can just go outside without taking an umbrella.' + '\n'
            bot.send_message(message.chat.id,reply12)

    except KeyError:
        bot.send_message(message.chat.id,'Sorry, it seems that you did tell me a correct city name. Please try again!  T_T')
    except IndexError:
        bot.send_message(message.chat.id,'Sorry, I can only give you weather forecast in five days. The date you want to know seems to be out of range!  ~_~')

INIT = 0
WANT_LOCATION = 1
WANT_DATE = 2
WANT_LOCATION_DATE = 3
FIND_WEATHER = 4
global params
params = {}
global state
state = INIT

policy = {
    (INIT, "no_location"): (WANT_LOCATION, "sorry, you didn\'t tell me which city did you want to know about! \n so please tell me more information! especially location! ^_^"),
    (INIT, "get_location_date"): (FIND_WEATHER, "Well, please wait for a few seconds!"),
    (INIT, "no_date"):(WANT_DATE, "sorry, it seems that you didn't tell me which day's weather do you want to know about"),
    (INIT, "no_location_date"): (WANT_LOCATION_DATE, "Excuse me, I am not sure which city and which day's weather do you want to know!"),
    (WANT_LOCATION, "get_location_date"): (FIND_WEATHER, "perfect, Please wait a few seconds!"),
    (WANT_LOCATION, "no_location"): (WANT_LOCATION, "sorry I still don't know the city you want to know about!"),
    (WANT_LOCATION,"no_date"): (WANT_DATE,"sorry, though I know the location you want to find, you still need to tell me which day's weather do you want to know about!"),
    (WANT_DATE,"get_location_date"): (FIND_WEATHER, "excellent! please wait for a few seconds!"),
    (WANT_DATE, "no_date"): (WANT_DATE, "sorry I still don't know the date you want to know about!"),
    (WANT_LOCATION_DATE,"get_location_date"):(FIND_WEATHER,"Fantastic, please wait a few seconds!"),
    (WANT_LOCATION_DATE,"no_location_date"):(WANT_LOCATION_DATE,"sorry, I still do not know either the city or date you want!")
}

#chat
@bot.message_handler()
def echo(message):
    global state
    global params
    #print(message)
    #print(type(message))
    message_text = message.text
    #print(message_text)
    # Check if the message is in the ask_name
    if message_text in ask_name:
        # Return a random matching response
        bot_message = random.choice(ask_name[message_text])
        bot.reply_to(message, bot_message)
        return None

    reply = respond_rules(message_text)
    if reply != message_text:
        bot.reply_to(message, reply)
        return None

    data = rasa_train(message_text)
    #print(data)
    if data['intent']['name'] == 'greet':
        # Find the name
        name = find_name(message_text)
        if name is None:
            answer = random.choice(say_hello["no_name"])
        else:
            answer = random.choice(say_hello["with_name"]).format(name)
        bot.reply_to(message, answer)
        return None
    if data['intent']['name'] == 'goodbye':
        answer = random.choice(say_goodbye['bye'])
        bot.reply_to(message, answer)
        return None
    if data['intent']['name'] == 'weather_search':
        print(state)
        # Extract the entities
        entities = data['entities']
        # Initialize an empty params dictionary
        #params = {}
        # Fill the dictionary with entities
        for ent in entities:
            params[ent["entity"]] = str(ent["value"])
        if "location" not in params and "date" in params:
            interpret = "no_location"
            state, respond = policy[(state,interpret)]
            bot.reply_to(message, respond)
        elif "location" in params and "date" not in params:
            interpret = "no_date"
            state, respond = policy[(state,interpret)]
            bot.reply_to(message,respond)
        elif "location" not in params and "date" not in params:
            interpret = "no_location_date"
            state, respond = policy[(state, interpret)]
            bot.reply_to(message, respond)
        elif "location" in params and "date" in params:
            interpret = "get_location_date"
            state, respond = policy[(state, interpret)]
            bot.reply_to(message, respond)
        if state == FIND_WEATHER:
            location = params["location"]
            date = params['date']
            weather = None
            if 'weather' in params:
                weather = params["weather"]
            if date == "today":
                current_weather(message, location, weather)
            elif date == "tomorrow":
                forecast_weather(message, location, 1, weather)
            elif "two" in date:
                forecast_weather(message, location, 2, weather)
            elif "three" in date:
                forecast_weather(message, location, 3, weather)
            elif "four" in date:
                forecast_weather(message, location, 4, weather)
            elif "five" in date:
                forecast_weather(message, location, 5, weather)
            state = INIT
            params ={}
        print(state)
        return None





if __name__ == '__main__':
    bot.polling()



