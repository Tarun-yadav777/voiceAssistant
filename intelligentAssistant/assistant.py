import pyttsx3
import speech_recognition as sr
import datetime
import calendar
import subprocess
import smtplib
import configparser
import requests
import json
from scrapper import scrapperFunction

import wolframalpha
from twilio.rest import Client

config = configparser.ConfigParser()
config.read('config.ini')


class MyAssistant:

    def __init__(self, voiceNum):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voiceNum].id)
        self.recognizer = sr.Recognizer()

    def talk(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    @staticmethod
    def wakeWord(text):
        actionWord = 'Assistant'
        text = text.lower()
        if actionWord in text:
            return True
        return False

    def recAudio(self):

        with sr.Microphone() as source:
            # self.recognizer.energy_threshold = 1000
            # self.recognizer.adjust_for_ambient_noise(source, 1.2)
            print("Listening...")
            audio = self.recognizer.listen(source)
        data = ''

        try:
            data = self.recognizer.recognize_google(audio)
            print(data)
            return data
        except sr.UnknownValueError:
            print('Could Not understand what you were saying... Sorry!')
        except sr.RequestError as ex:
            print('Request error from Google Speech Recognition' + ex)

    @staticmethod
    def todayDayAndDate():
        now = datetime.datetime.now()
        dateNow = datetime.datetime.today()
        weekNow = calendar.day_name[dateNow.weekday()]
        monthNow = now.month
        dayNow = now.day
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                  'August', 'September', 'October', 'November', 'December']
        ordinals = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                    '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
                    '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
                    '29th', '30th', '31st']
        return 'Today is {}, {} {}.'.format(weekNow, months[monthNow - 1], ordinals[dayNow - 1])

    @staticmethod
    def greet(text):

        greetList = ['hi', 'hey', 'hello', 'hello there', 'hola', 'howdy', 'wassup', 'greeting']
        response = 'Hey there! Welcome.'
        for word in text.split():
            if word.lower() in greetList:
                return response
        return ""

    @staticmethod
    def wikiPerson(text):
        listWiki = text.split()
        for i in range(0, len(listWiki)):
            if (i + 3 <= len(listWiki) - 1) and (listWiki[i].lower() == 'who') and (listWiki[i + 1].lower() == 'is'):
                return listWiki[i + 2] + ' ' + listWiki[i + 3]

    @staticmethod
    def note(text):
        date = datetime.datetime.now()
        fileName = str(date).replace(':', "-") + "-note.txt"
        with open(fileName, 'w') as f:
            f.write(text)

        subprocess.Popen(['notepad.exe', fileName])

    @staticmethod
    def sendEmail(to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()

        server.login('email', 'password')
        server.sendmail('email', to, content)
        server.close()

    @staticmethod
    def getWeather(text):
        key = config['api']['weatherKey']
        ind = text.split().index('in')
        location = text.split()[ind + 1:]
        location = ' '.join(location)
        URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'.format(location, key)
        js = requests.get(URL).json()
        if js['cod'] != 404:
            weather = js['main']
            temperature = weather['temp']
            temperature = int(temperature - 273.15)
            humidity = weather['humidity']
            desc = js['weather'][0]['description']
            return 'Temperature is {} Celcius, Humidity is {} and Weather description is {}'.format(temperature,
                                                                                                    humidity, desc)
        return "City not found."

    def getNews(self):
        key = config['api']['newsKey']
        URL = 'https://newsapi.org/v2/top-headlines?country=in&apiKey={}'.format(key)
        try:
            response = requests.get(URL)
        except Exception as e:
            print(e)
            print('Please check your connection')

        news = json.loads(response.text)
        for new in news['articles']:
            print(str(new['title']), "\n")
            self.talk(str(new['title']))

            print(str(new['description']), "\n")
            self.talk(str(new['description']))

    def sendMessage(self):
        accountSID = config['twilio']['sid']
        token = config['twilio']['token']
        fromNum = config['twilio']['from']
        toNum = config['twilio']['to']
        client = Client(accountSID, token)

        self.talk('What should i send?')

        message = client.messages.create(body=self.recAudio(), from_=fromNum, to=toNum)

        return 'Message send successfully'

    @staticmethod
    def getAns(text):
        appID = config['api']['appID']
        client = wolframalpha.Client(appID)
        ind = text.lower().split().index('calculate')
        text = text.split()[ind + 1:]
        res = client.query(" ".join(text))
        print(res)
        answer = next(res.result).text
        return answer

    @staticmethod
    def getAns2(text):
        appID = config['api']['appID']
        client = wolframalpha.Client(appID)
        ind = text.lower().split().index('is')
        text = text.split()[ind + 1:]
        res = client.query(" ".join(text))
        print(res)
        answer = next(res.results).text
        return answer

    def getSchemes(self, keyword):
        schemeList = scrapperFunction(keyword)
        for scheme in schemeList.keys():
            # print(scheme)
            self.talk(scheme)

    def diagnose(self, patientSymptoms, gender, dob):
        print('in function')
        token = config['api']['token']
        symptomID = None
        symptomURL = 'https://sandbox-healthservice.priaid.ch/symptoms?token={}&format=json&language=en-gb'.format(token)

        # try:
        symptomsResponse = requests.get(symptomURL)
        symptoms = symptomsResponse.json()
        for symptom in symptoms:
            if symptom['Name'].lower() == patientSymptoms:
                symptomID = symptom['ID']

        diagnoseURL = 'https://sandbox-healthservice.priaid.ch/diagnosis?symptoms=[{}]&gender={}&year_of_birth={}&token={}&format=json&language=en-gb'.format(
            symptomID, gender, dob, token)
        diagnoseResponse = requests.get(diagnoseURL)
        diagnoses = diagnoseResponse.json()
        for diagnose in diagnoses:
            print("{} ::: {}".format(diagnose['Issue']['Name'], diagnose['Issue']['IcdName']))
                # self.talk('Disease may be {} which is {]'.format(diagnose['Issue']['Name'], diagnose['Issue']['IcdName']))
        # except Exception as e:
        #     print(e)
        #     print('Error in finding cure')

