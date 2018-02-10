# -*- coding: utf-8 -*-
import config
import telebot
import random
import requests
# import json


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    print("{0}, {1}".format(message.location.latitude, message.location.longitude))


@bot.message_handler(content_types=['text'])
def botsystem(message):

    def weather():

        def meteoConditionDescr(meteoCode):

            conditionJSON = [
                {'En': 'Thunderstorm', 'Ru': u'гроза'},
                {'En': 'Drizzle',      'Ru': u'изморось'},
                {'En': 'Rain',         'Ru': u'дождь'},
                {'En': 'Snow',         'Ru': u'снег'},
                {'En': 'Clear',        'Ru': u'ясно'},
                {'En': 'Clouds',       'Ru': u'облачно'}
            ]

            iFound = False
            conditionName = ""
            for i in range(0, len(conditionJSON)):
                if meteoCode == conditionJSON[i]['En']:
                    iFound = True
                    conditionName = conditionJSON[i]['Ru']

            return conditionName if iFound else 'X'


        def wind(degrees):
            degreesJSON = [
                # {'degree': 360,    'name': 'северный'},
                {'degree': 22.5,   'name': u'северo-северо-восточный'},
                {'degree': 45,     'name': u'северо-восточный'},
                {'degree': 67.5,   'name': u'восточный-северо-восточный'},
                {'degree': 90,     'name': u'восточный'},
                {'degree': 112.5,  'name': u'восточный-юго-восточный'},
                {'degree': 135,    'name': u'юго-восточный'},
                {'degree': 157.5,  'name': u'юго-юго-восточный'},
                {'degree': 180,    'name': u'южный'},
                {'degree': 202.5,  'name': u'юго-юго-западный'},
                {'degree': 225,    'name': u'юго-западный'},
                {'degree': 247.5,  'name': u'западный-юго-западный'},
                {'degree': 270,    'name': u'западный'},
                {'degree': 292.5,  'name': u'западный-северо-западный'},
                {'degree': 315,    'name': u'северо-западный'},
                {'degree': 337.5,  'name': u'северо-северо-западный'},
            ]
            windDirection = ''
            iFound = False
            if (degrees > 347.75 and degrees <= 360) or (degrees >= 0 and degrees <= 12.25):
                iFound = True
                windDirection = u'северный'
            else:
                for i in range(0, len(degreesJSON)):
                    oneValue = degreesJSON[i]
                    if degrees > oneValue['degree'] - 12.25 and degrees <= oneValue['degree'] + 12.25:
                        iFound = True
                        windDirection = oneValue['name']

            return windDirection if iFound else u'какой-то непонятный, наверное, сверху вниз...'

        try:
            city = 'Moscow,ru'
            appid = 'ab930bccc92605497e8a43b03e01545b'
            addParams = '&units=metric'
            weatherUrl = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + appid + addParams
            weatherRequest = requests.get(weatherUrl)
            weatherJSON = weatherRequest.json()
            # print(weatherJSON)
            temperatureTodayMin = str(weatherJSON['main']['temp_min'])
            temperatureTodayMax = str(weatherJSON['main']['temp_max'])
            atmospherePressure = weatherJSON['main']['pressure']
            meteoConditionCode = weatherJSON['weather'][0]['main']
            meteoCondition = meteoConditionDescr(meteoConditionCode)
            pressureDelimeter = 101325.0 / 760.0
            atmospherePressureHg = str(round((atmospherePressure * 100) / pressureDelimeter))
            humidity = str(weatherJSON['main']['humidity'])
            windSpeed = str(weatherJSON['wind']['speed'])
            windDirection = weatherJSON['wind']['deg']


            if meteoCondition != 'X':
                textCondition = u'Сейчас в Москве ' + meteoCondition + '. \n'
            else:
                textCondition = ''

            textTemperature = u'Температура воздуха от ' + temperatureTodayMin + \
                              u'°C до ' + temperatureTodayMax + '°C. \n'
            textPressure = u'Атмосферное давление ' + atmospherePressureHg + \
                           u' мм. рт. ст. \n'
            textHumidity = u'Относительная влажность воздуха ' + humidity + '%. \n'
            if int(windSpeed) > 0:
                textWind = u'Ветер ' + wind(windDirection) + u', скорость ' + windSpeed + u' м/с. \n'
            else:
                textWind = ''

            fullText = textCondition + textTemperature + textPressure + textHumidity + textWind
            return fullText
        except:
            return u'Простите, кажется, наш дежурный шаман порвал бубен. \n' + \
                   u'Попробуйте позже, он уже пошёл за новым.'


    def answerPerson(text):
        text = text.lower()
        dialogue = [
            {
                'man': [
                    u'привет',
                    u'здравствуй',
                    u'ку',
                    u'здорово',
                    u'хай'
                ],
                'bot': [
                    u'Привет-привет!',
                    u'Здравствуйте!',
                    u'И вам не хворать!',
                    u'Ба! Какие люди!'
                ]
            },
            {
                'man': [
                    u'как дела',
                    u'чокак',
                    u'как ты',
                    u'как поживаешь',
                    u'как сам',
                    u'чо почём'
                    u'как поживаешь'
                ],
                'bot': [
                    u'Прекрасно! Надеюсь, что и у тебя тоже!',
                    u'Всё круто, спасибо!',
                    u'Не дождётесь...',
                    u'Всё отлично, йей!']
            },
            {
                'man': [
                    u'как тебя зовут',
                    u'ты кто',
                    u'кто ты'
                ],
                'bot': [
                    u'Меня зовут Тестовый Бот Амиборов!',
                    u'Я просто тестовый бот.',
                    u'Я тот, кто желает зла, но вечно творит благо... Ну или как его там.'
                ]
            },
            {
                'man': [
                    u'до свидания',
                    u'пока',
                    u'досвидания',
                    u'досвидос',
                    u'бывай'
                ],
                'bot': [
                    u'Доброго здоровьичка!',
                    u'Пока-пока!',
                    u'Честь имею откланяться!',
                    u'Всего доброго!',
                    u'Чмоки-чмоки!'
                ]
            }
        ]
        iFound = False

        myAnswer = ''

        for i in range(0, len(dialogue)):
            oneManSaySet = dialogue[i]['man']
            for j in range(0, len(oneManSaySet)):
                oneManSay = oneManSaySet[j]
                if oneManSay in text:
                    iFound = True
                    answerNumber = random.randint(0, len(dialogue[i]['bot']) - 1)
                    myAnswer = dialogue[i]['bot'][answerNumber]

        if iFound:
            return myAnswer
        else:
            return 'Ooops...'

    if u'погода' in message.text.lower():
        fullMsg = weather()
    else:
        fullMsg = answerPerson(message.text)

    bot.send_message(message.chat.id, fullMsg)


if __name__ == '__main__':
     bot.polling(none_stop=True)
