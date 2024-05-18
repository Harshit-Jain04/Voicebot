import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import smtplib
import wikipedia
import os

today = date.today()
r = sr.Recognizer()
keyboard = Controller()
engine = pyttsx3.init('sapi5')
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def reply(audio):
    
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        reply("Good Morning!")
    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   
    else:
        reply("Good Evening!")  
        
    reply("How may I help you?")

# Set Microphone parameters
#def start():
#     with sr.Microphone() as source:
#        print("Listening for user input...")
#        r.adjust_for_ambient_noise(source)
#        audio = r.listen(source)
#        try:
#            voice = r.recognize_google(audio)
#            print(voice)
#            if 'activate' in voice.lower():
#                record_audio()
#        except:
#            pass
        
active = False
# Audio to String
def record_audio():
    global active
    with sr.Microphone() as source:
        r.energy_threshold = 500 
        r.dynamic_energy_threshold = False
        r.pause_threshold = 0.8
        voice_data = ''

        try:
            audio = r.listen(source)
            voice_data = r.recognize_google(audio)
            print(voice_data)
            if 'harshit' in voice_data.lower() or 'harshad' in voice_data.lower():
                active = True
                
            if active:
                respond(voice_data.lower())
        except sr.WaitTimeoutError:
            pass
        except sr.RequestError:
            reply('Sorry my Service is down. Plz check your Internet connection')
        except sr.UnknownValueError:
            reply('sorry i cant recognize that')
            pass
    return


# Executes Commands (input: string)
def respond(voice_data):
    global active
    #print(voice_data)
    
    # STATIC CONTROLS
    if 'type' in voice_data:
        data = voice_data.split('type')[1]
        data = data.lower()
        print(data)
        for i in data:
            keyboard.press(i)
            keyboard.release(i)
    elif 'hello' in voice_data:
        wish()
    
    elif 'what is your name' in voice_data:
        reply('My name is Voice bot. I am made by Harshit.')

    elif 'date' in voice_data:
        reply("Today's date is "+today.strftime("%B %d, %Y"))

    elif 'time' in voice_data:
        reply("Current time is "+str(datetime.datetime.now()).split(" ")[1].split('.')[0])
    
    elif 'open' in voice_data:
        app_name = voice_data.split("open")[1].lower()
        try:
            if "chrome" in app_name.lower():
                os.system("start chrome")
                reply(f'opening {app_name}')

            elif "notepad" in app_name.lower():
                os.system("start notepad")
                reply(f'opening {app_name}')
            else:
                os.system(f'start {app_name}')
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    elif 'google' in voice_data:
        reply("Searching for"+voice_data.replace('google','')+" on google")
        url = 'https://google.com/search?q=' + voice_data.replace('google','')
        try:
            webbrowser.get().open(url)
            reply('this is what i found')
        except:
            reply('Check your internet connection')
    elif 'youtube' in voice_data:
        reply("Searching for"+voice_data.replace('youtube','')+" on youtube")
        url = "https://www.youtube.com/results?search_query="+voice_data.replace('youtube','')
        try:
            webbrowser.get().open(url)
            reply('this is what i found')
        except:
            reply('Check internet connection')
    elif 'search' in voice_data:
        try:
            result= wikipedia.summary(voice_data.replace('search',''),sentences = 3)
            reply(result)
        except wikipedia.exceptions.PageError:
            url = 'https://google.com/search?q=' + voice_data.replace('search','')
            try:
                webbrowser.get().open(url)
                reply('this is what i found')
            except:
                reply('Check your internet connection')

    elif 'location' in voice_data:
        #reply('Which place are you looking for ?')
        #temp_audio = record_audio()
        temp_audio=voice_data.split('location')[1]
        reply('Locating...')
        url = 'https://google.nl/maps/place/' + temp_audio + '/&amp;'
        try:
            webbrowser.get().open(url)
            reply('This is what I found Sir')
        except:
            reply('Please check your Internet')
        
    elif 'copy' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('c')
            keyboard.release('c')
        reply('Copied')
          
    elif 'page' in voice_data or 'pest'  in voice_data or 'paste' in voice_data:
        with keyboard.pressed(Key.ctrl):
            keyboard.press('v')
            keyboard.release('v')
        reply('Pasted')
    
    
    elif 'press' in voice_data or 'click' in voice_data:
        x = voice_data.split('press')[1].lower()
        x = x.strip()
        key_replacements = {
    'control': Key.ctrl,
    'escape': Key.esc,
    'caps lock': Key.caps_lock,
    'left': Key.left,
    'right': Key.right,
    'up': Key.up,
    'down': Key.down,
    'page up': 'pageup',
    'page down': 'pagedown',
    'print screen': 'printscreen',
    'scroll lock': 'scrolllock',
    'shift':Key.shift,
    'tab':Key.tab,
    'windows':Key.cmd,
    'enter':Key.enter,
    'alt':Key.alt
}
        ke = key_replacements.keys()
        try:
            if '+' in x or 'plus' in x:
                keys= x.split('+') if '+' in x else x.split('plus')
                if keys[-1]!="":
                    for ik in range(0,len(keys)):
                        keys[ik] = keys[ik].strip()
                        if keys[ik] in ke:
                            keys[ik] = key_replacements.get(keys[ik])
                    print(keys)
                    for key in keys:
                        keyboard.press(key)
                    keys.reverse()
                    for key in keys:
                        keyboard.release(key)
            else:
                if x in ke:
                    keyboard.press(key_replacements.get(x))
                    keyboard.release(key_replacements.get(x))
                else:
                    if len(x)==1:
                        keyboard.press(x)
                        keyboard.release(x)
        except ValueError:
            reply('please repeat command')
    elif 'deactivate' in voice_data:
        reply('deactivated')
        active=False
    elif 'harshit' in voice_data or 'harshad' in voice_data:
        wish()
    else: 
        reply('I am not functioned to do this !')
    
while(True):
    record_audio()
