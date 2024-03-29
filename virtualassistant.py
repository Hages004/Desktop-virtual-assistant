# Sample desktop virtual assistant code

from PyQt5.QtWidgets import QWidget
import pyttsx3
import datetime
import speech_recognition as sr
import os
import wikipedia
import pywhatkit
import subprocess
import pyjokes
import webbrowser
import ctypes
import time
import keyboard
import pyautogui



# Constants for Windows API
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
VK_BRIGHTNESS_UP = 0x6F
VK_BRIGHTNESS_DOWN = 0x70

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty ('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def command():
    r=sr.Recognizer() # using the recognizer which is inside the sr module
    with sr.Microphone()as source: 
        print("How can i help you") # this will be displayed when ever the microphone is on
        r.pause_threshold = 1 # To correct the fault which will occur in the mocrophone and it will take the input with gaps
        r.adjust_for_ambient_noise(source, duration=1) 
        audio=r.listen(source) 
    try:
        print("Wait for a minute")
        query=r.recognize_google(audio, language='en-in')
        print("You just said",query) 
    except Exception as e:
        print(e)
        speak("tell me again")
        query=command() 
    return  query
def wakeup():
    r=sr.Recognizer() # using the recognizer which is inside the sr module
    with sr.Microphone()as source: 
        print("sleeping......") # this will be displayed when ever the microphone is on
        r.pause_threshold = 1 # To correct the fault which will occur in the mocrophone and it will take the input with gaps
        r.adjust_for_ambient_noise(source, duration=1) 
        audio=r.listen(source) 
    try:
        
        query=r.recognize_google(audio, language='en-in')
        print("You just said",query) 
    except Exception as e:
                
        query=command() 
    return query

def wishing():
    h=int(datetime.datetime.now().hour)
    if h>=0 and h<=11:
        speak("Good Morning")
        print("Good morning")
    elif h>=12 and h<=17:
        speak("Good Afternoon")
        print("Good Afternoon")
    elif h>=18 and h <=22:
        speak("Good Evening")
        print("Good Evening")

def open_calculator():
    subprocess.Popen(['calc.exe'])
    speak('Opening Calculator')   

def type_in_word(text):
    os.system("start winword")
    time.sleep(1)
    keyboard.write(text)

def perform_calculator_operation(operation):
    subprocess.Popen(['calc.exe'])
    time.sleep(1)
    keyboard.write(operation)
    keyboard.press_and_release('enter')    

def adjust_volume(up=True):
    # Adjust volume using Windows API
    key = VK_VOLUME_UP if up else VK_VOLUME_DOWN
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    ctypes.windll.user32.keybd_event(key, 0, 0x0002, 0)  

def adjust_volume(up=True):
    # Adjust volume using Windows API
    key = VK_VOLUME_UP if up else VK_VOLUME_DOWN
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    ctypes.windll.user32.keybd_event(key, 0, 0x0002, 0)

def adjust_brightness(up=True):
    # Adjust brightness using Windows API
    key = VK_BRIGHTNESS_UP if up else VK_BRIGHTNESS_DOWN
    ctypes.windll.user32.keybd_event(key, 0, 0, 0)
    ctypes.windll.user32.keybd_event(key, 0, 0x0002, 0)    

def get_wikipedia_info(query):
    try:
        info = wikipedia.summary(query, sentences=1)
        return info
    except wikipedia.DisambiguationError as e:
        return f"Multiple results found. Please be more specific. {e}"
    except wikipedia.PageError as e:
        return f"Could not find any information on {query}. {e}"      
                
if __name__ == "__main__":
    while True:
        wishing()
        speak("How can i help you")
        query = command().lower()

        if 'wake up ' in query:
            wishing()
            speak("what can i do for you")
            while True:
                query = command().lower()
                if 'time'in query:
                    speak('Current time is ' + str(datetime.datetime.now().strftime('%I:%M %p')))  

                elif 'go to sleep' in query:
                    speak("Ok i'm going to sleep, if there's anything else I can help you with, just call me")
                    wakeup()
                    

                elif 'open chrome' in query:
                    os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")   
                    while True:
                        chrome = command().lower()
                        if 'search' in chrome:
                            youtube=chrome
                            youtube=youtube.replace("search","")
                            pyautogui.write(youtube)
                            pyautogui.press('enter')
                            speak("Searching.......")
                        elif 'exit google' in chrome or 'exit chrome' in chrome:
                            pyautogui.hotkey("ctrl","w")    
                            speak("Closing google")
                            break
                elif 'Who is'in query:
                    speak("searching in wikipedia")
                    try:
                        query=query.replace('wikipedia',' ')
                        results=wikipedia.summary(query, sentences  =1)
                        speak("According to wikipedia")
                        print(results)
                        speak(results) 
                    except:
                        print("No results found") 

                elif 'perform calculator operation' in query:
                    operation = query.replace('perform calculator operation', '')
                    perform_calculator_operation(operation)             

                elif 'play' in query:
                    playquery=query.replace('play',' ')      
                    speak("playing"+playquery)
                    pywhatkit.playonyt(playquery)

                elif 'open notepad' in query:
                    subprocess.Popen(['notepad.exe'])
                    speak('Opening Notepad')
                        
                elif 'open calculator' in query:
                    open_calculator()

                elif 'open file explorer' in query:
                    subprocess.Popen(['explorer.exe'])
                    speak('Opening File Explorer')

                elif 'tell me a joke' in query:
                    speak('Here is a joke for you: ' + str(pyjokes.get_joke()))       

                elif 'minimise' in query or 'minimize'in query:
                    speak('Minimizing...')
                    pyautogui.hotkey("win","down","down")
                        
                elif 'maximise'in query or 'maximize' in query:
                    speak("Maximizing....")   
                    pyautogui.hotkey("win", "up","up")
                        
                elif 'close current window'in query or 'close the current window'in query:
                    speak("Closing the window....")
                    pyautogui.hotkey("ctrl","w")

                elif 'screen shot'in query:
                    speak("Taking a screen shot")
                    pyautogui.press("prtsc")

                elif 'exit'in query or 'exit the program' in query:
                    speak("I'm leaving byee.....")         
                    quit()
        
                elif 'type in word' in query:
                    speak("what should i type in the word document?")
                    text_to_type=command()
                    os.system("start winword")
                    time.sleep(1)# Allowing time for word to open
                    keyboard.write(text_to_type)

                elif 'increase volume' in query:
                    adjust_volume(up=True)
                    speak('Increasing volume')

                elif 'decrease volume' in query:
                    adjust_brightness(up=False)
                    speak('Decreasing volume')    

                elif 'increase brightness' in query:
                    adjust_brightness(up=True)
                    speak('Increasing brightness')
            
                elif 'decrease brightness' in query:
                    adjust_brightness(up=False)
                    speak('Decreasing brightness')

                elif 'who is' in query:
                    person = query.replace('who is', '')
                    speak('Searching Wikipedia...')
                    info = get_wikipedia_info(person)
                    speak(info)    

                elif 'what is' in query:
                    person = query.replace('what is', '')
                    speak('Searching Wikipedia...')
                    info = get_wikipedia_info(person)
                    speak(info)      

                elif 'which is' in query:
                    person = query.replace('which is', '')
                    speak('Searching Wikipedia...')
                    info = get_wikipedia_info(person)
                    speak(info)          

                elif 'thank you' in query:
                    speak("You're welcome! if there's anything else I can help you with, feel free to ask.")
                    print("You're welcome! if there's anything else I can help you with, feel free to ask.") 
                    quit() 
command()                    

