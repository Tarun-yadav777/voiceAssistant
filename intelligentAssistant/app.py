from assistant import MyAssistant
import datetime
import wikipedia


if __name__ == '__main__':

    assistant = MyAssistant(0)

    while True:
        try:
            text = assistant.recAudio()
            speak = ''

            speak = speak + assistant.greet(text)

            if ('date' in text) or ('month' in text) or ('day' in text):
                getToday = assistant.todayDayAndDate()
                speak = speak + " " + getToday
            elif 'time' in text:
                now = datetime.datetime.now()
                meridiem = ''
                if now.hour >= 12:
                    meridiem = 'p.m'
                    hour = now.hour - 12
                else:
                    meridiem = 'a.m'
                    hour = now.hour
                if now.minute < 10:
                    minute = '0' + str(now.minute)
                else:
                    minute = str(now.minute)
                speak = speak + " " + "It is " + str(hour) + ":" + minute + " " + meridiem + '.'
            elif 'wikipedia' in text:
                if 'who is' in text:
                    person = assistant.wikiPerson(text)
                    wiki = wikipedia.summary(person, sentences=2)
                    speak = speak + " " + wiki

            elif ('who are you' in text) or ('what are you' in text):
                speak = speak + ' ' + 'I am a Bot, Your Assistant. Here to help you.'

            elif ('note' in text) or ('remember' in text):
                assistant.talk('What would you like me to note down for you?')
                noteText = assistant.recAudio()
                assistant.note(noteText)
                speak = speak + 'I have created a note.'
            
            elif ('mail' in text) or ('gmail' in text) or ('email' in text):
                try:
                    assistant.talk('What should i mail?')
                    content = assistant.recAudio()
                    assistant.talk('Please enter the address of reciver mail.')
                    to = input('Email address of reciver=> ')
                    assistant.sendEmail(to, content)
                    speak = speak + 'Email has been sent'
                
                except Exception as e:
                    print(e)
                    assistant.talk('Not able to send email because of below mention error.')

            elif 'weather' in text:
                response = assistant.getWeather(text)
                speak = speak+response

            elif 'news' in text:
                assistant.getNews()

            elif ('send message' in text) or ('send a message' in text):
                response = assistant.sendMessage()
                speak = speak+response

            elif 'calculate' in text:
                response = assistant.getAns(text)
                speak = speak+"Answer is "+response

            elif ('what is' in text) or ('who is' in text):
                response = assistant.getAns2(text)
                speak = speak+response

            elif ("scheme" in text) or ('government' in text):
                assistant.talk('What kind of schemes you looking for?')
                schemeKeyword = assistant.recAudio()
                print(schemeKeyword)
                assistant.getSchemes(schemeKeyword)

            elif ('health' in text) or ('cure' in text) or ('treatment' in text) or ('medical' in text):
                assistant.talk('Do you want me with your medical problem?')
                if "yes" in assistant.recAudio().lower():
                    assistant.talk('Can you tell me your symptoms')
                    symptom = assistant.recAudio()
                    assistant.talk('Tell your age')
                    age = assistant.recAudio()
                    age = int(age)
                    by = datetime.datetime.now().year-age
                    assistant.talk('Are you female?')
                    genderQ = assistant.recAudio()
                    if 'no' in genderQ.lower():
                        gender = 'male'
                    else:
                        gender = 'female'
                    assistant.talk('Wait few seconds let me find disease related to your symptoms')
                    assistant.diagnose(symptom, gender, by)



            assistant.talk(speak)
        except Exception as e:
            # assistant.talk("Sorry! Can you repeat.I Didn't Understand that.")
            print(e)
            print("Sorry! Can you repeat.I Didn't Understand that.")
