import pyttsx3 as textToSpeech
import speech_recognition as sr

engine = textToSpeech.init()

# engine.say('Hello taronic.')
# engine.runAndWait()
# 
#
# voiceSpeedRate = engine.getProperty('rate')
# engine.setProperty('rate', 100)
#
# print('Speed Rate of Previous Voice: {} and now is 100'.format(voiceSpeedRate))
#
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
#
# engine.say('Hello taronic.')
# engine.runAndWait()


def speak(text):
    engine.say(text)
    engine.runAndWait()

r = sr.Recognizer()

speak("Konichiwa Taronic san, i am at your service senpai. ")
with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, 1.2)
    print('listening ....')
    audio = r.listen(source)
    text = r.recognize_google(audio)
    print(text)