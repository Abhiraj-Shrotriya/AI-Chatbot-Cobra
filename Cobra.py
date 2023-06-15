#pip install SpeechRecognition
#pip install gTTS
#pip install wikipedia

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import calendar
import random
import wikipedia
import warnings
import csv


warnings.filterwarnings('ignore')




def recordaudio():
    data = ''
    if Mode=='Text':
        data = input("Enter your query : ")
    elif Mode=='Speech':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say Something...')
            audio = r.listen(source,4,3)
        #speechrecognition using google
        
        try:
            data = r.recognize_google(audio)
            print('You said:'+data)
        except sr.UnknownValueError:
            print('sorry,Could not understand that')
        except sr.RequestError as e:
            print('results of error:'+e)
    return data

        
#function to get audio response from the AI
def AIresponse(text):
    print('Chatbot Says :',text)
    if status == 'Muted':
        pass
    else:
        #converting the text to audio
        myobj = gTTS(text = text, lang = 'en', slow= False)

        #saving the converted audio
        myobj.save('AIresponse.mp3')

        #playing the audio
        os.system('start AIresponse.mp3')

#function to check for wake words
def wakeword(text):
    wake_words = ['hey computer',"hi computer","computer","hay computer","hai computer","a computer"]
    text = text.lower()
    
    for phrase in wake_words:
        if phrase in text:
            return True
    return False

#function to check the date
def get_date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthnum = now.month
    daynum = now.day
    year = datetime.date.today().year
    #the list of months
    month_names = ['january', 'feburary', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 
                   'december']
    #list of ordinal nums
    ordinalnums = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th','14th',
                  '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23th', '24th', '25th', '26th', '27th',
                  '28th', '29th', '30th', '31st']
    return 'Today is '+weekday+' '+ordinalnums[daynum - 1]+' '+month_names[monthnum - 1]+' '+str(year)+'.'


#function to generate a random greeting
def greeting(text):
    
    GREETING_INPUTS = ['hi', 'hello', 'greetings', 'whats up', 'hey']
    
    GREETING_RESPONSES = ['hi', 'hello', 'whats up', 'what is going on', 'hey dude', 'hey there']
    
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)+'.'
        
        
        return ''


#function to get an information on a person/thing
def getwiki(text):
    
    wordlist = text.split() #split the text into a list of words
    wordlist.append(' ')
    
    getter = ''
    for i in range(0,len(wordlist)):
        
        if (wordlist[i]== 'who' or wordlist[i]=='what') and (wordlist[i+1]=='was' or wordlist[i+1]=='is' or wordlist[i+1]=='are'):
            try:
                getter = wordlist[i+2]+' '+wordlist[i+3]+' '+wordlist[i+4]
            
            except:
                try:
                    getter = wordlist[i+2]+' '+wordlist[i+3]
                except:
                    getter = wordlist[i+2]+' '
        
        else:
            pass
    
    
    wiki = wikipedia.summary(getter, sentences = 2)
    
    return wiki



def main_func():
    text = recordaudio()
    tq = str(text)
    global response
    response = ' \n'
    l = []
    l1 = []
    try:
        with open(r'tfile.csv','r',newline='',encoding="utf-8") as f:
            a = csv.reader(f)
            l = [x for x in a]
            l1 = [x[0] for x in l]
            
    except:
        pass
    if text in l1:
        response = response+l[l1.index(text)][1]
    elif (wakeword(text)== True):
        response = response +greeting(text)
        
        if('date' in text):
            getdate = get_date()
            response = response + ' '+ getdate
        elif('time' in text):
            hour=0
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour>=12:
                meridiem = 'PM'
                hour = now.hour - 12
            else:
                meridiem = 'AM'
                
            response = response+'It is '+ str(hour)+':'+str(now.minute)+' '+meridiem
        
        #checking if user said who is
        elif('who is'or 'who was' or 'what is' or 'what are' in text):
            
            response = response + ' '+getwiki(text)
        else:
            pass
        
    elif greeting(text) != '' and greeting(text) != None:
        response = response +greeting(text)
    
    
    afq = response.replace(' \n','')
    try:
        with open(r'tfile.csv','a',newline = '',encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([str(tq),str(afq)])
    except:
        with open(r'tfile.csv','w',newline = '',encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([str(tq),str(afq)])
    
    AIresponse(response)
    
#def response_func():
#    AIresponse(response)

decider = bool(0)
response = ''
text = ''
outer_text = ''
Mode = 'Speech'
status = 'Unmuted'




def menu_function():
    global Mode
    global status
    try:
        with open(r'aisets.txt','r',newline = '') as f:
            a = csv.reader(f)
            p = True
            for i in a:
                if p == True:
                    Mode = i[1]
                elif p == False:
                    status = i[1]
                p = False
    except:
        Mode = 'Speech'
        status = 'Unmuted'
    print("\033[1m|.............................................MENU..............................................|\n")
    print('\033[1m1. Use Chatbot..................................................................................|','\n')
    print('\033[1m2. Train Chatbot................................................................................|\n')
    print('\033[1m3. Change Settings of Chatbot...................................................................|\n')
    print('\033[1m4. Exit.........................................................................................|\n',)
    
    mcom = int(input("Enter the number of the function that you want to use : "))
    if mcom == 1:
        main_func()
    if mcom == 2:
        train_bot()
    if mcom == 3:
        change_sets()
    else:
        print("Goodbye!")
    
def train_bot():
    tq = input("Enter train query : ")
    afq = input("Enter ideal response : ")
    try:
        with open(r'tfile.csv','a',newline='') as f:
            w = csv.writer(f)
            w.writerow([tq,afq])
    except:
        with open(r'tfile.csv','w',newline='') as f:
            w = csv.writer(f)
            w.writerow([tq,afq])
    
    menu_function()
def change_sets():
    global Mode
    global status
    try:
        with open(r'aisets.txt','r',newline = '') as f:
            a = csv.reader(f)
            p = True
            for i in a:
                if p == True:
                    Mode = i[1]
                elif p == False:
                    status = i[1]
                p = False
    except:
        Mode = 'Speech'
        status = 'Unmuted'
    print('These are the current settings : ')
    print('1. Mode = {}'.format(Mode))
    print('2. Mute/Unmute = {}'.format(status))
    print('3. Go back')
    a = int(input())
    if a==1:
        if Mode == 'Text':
            Mode = 'Speech'
        elif Mode == 'Speech':
            Mode = 'Text'
        print('Mode changed!')
        with open(r'aisets.txt','w',newline = '') as f:
            q = csv.writer(f)
            q.writerow(['Mode', Mode])
            q.writerow(['status',status])
        menu_function()
    if a==2:
        if status == 'Muted':
            status = 'Unmuted'
        elif status == 'Unmuted':
            status = 'Muted'
        print('status changed!')
        with open(r'aisets.txt','w',newline = '') as f:
            q = csv.writer(f)
            q.writerow(['Mode', Mode])
            q.writerow(['status',status])
        menu_function()
    if a==3:
        menu_function()

    with open(r'aisets.txt','w',newline = '') as f:
        q = csv.writer(f)
        q.writerow(['Mode', Mode])
        q.writerow(['status',status])

menu_function()


