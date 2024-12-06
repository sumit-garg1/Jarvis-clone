import pyttsx3
import speech_recognition as sp
from django.shortcuts import render
import time
import webbrowser
import os
from googlesearch import search

# Initialize the recognizer
listener = sp.Recognizer()

def speak(text):
    # Reinitialize the engine to avoid the "run loop already started" error
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1])  # Using default voice (index 0)
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Ensure the event loop is stopped after speaking

def get_command():
    print("Listening...")
    try:
        with sp.Microphone() as source:  # Use the microphone as the audio source
            listener.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = listener.listen(source)  # Listen to the audio input
            command = listener.recognize_google(audio, language="en-in")  # Convert audio to text
            print(f"Recognized command: {command}")
            return command.lower()
    except sp.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return None
    except sp.RequestError:
        print("Sorry, there was a network issue.")
        speak("Sorry, there was a network issue.")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        speak(f"An error occurred: {str(e)}")
        return None

def alexa(request):    
    if request.method == 'POST':
        command = get_command()

        if command is None:  # If no command is recognized, continue listening
            return render(request, "alexa.html")
        
        if 'hello jarvis' in command:
            speak("Hello Sir. I am Jarvis AI assistant. How may I help you?")
            return render(request, "alexa.html")

        # Handle 'play' command
        if 'who made you' in command:
            speak("I was created by Mr. Sumit Garg.")
            
        elif 'play' in command:
            song = command.replace('play', '').strip()
            speak(f"Playing {song} on YouTube.")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        # Handle 'time' command
        elif 'time' in command:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)
            speak(f"Current time is {current_time}")

        # Handle 'open' command (simplified to open websites or apps)
        elif 'open' in command:
            app = command.replace('open', '').strip()
            if 'youtube' in app:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com/")
            elif 'whatsapp' in app:
                speak("Opening WhatsApp")
                webbrowser.open("https://web.whatsapp.com/")
            elif 'calculator' in app:
                speak("Opening Calculator")
                if os.name == 'nt':  # For Windows
                    os.system('calc')
            elif 'notepad' in app:
                speak("Opening Notepad")
                if os.name == 'nt':  # For Windows
                    os.system('notepad')
            else:
                speak(f"Sorry, I can't open {app}.")

        # Handle 'information about' command
        elif 'information about' in command:
            query = command.replace('information about', '').strip()
            speak(f"Gathering information about {query}.")
            result = next(search(query), None)
            if result:
                webbrowser.open(result)
            else:
                speak(f"Sorry, I couldn't find any information about {query}.")

        else:
            speak("Sorry, I didn't understand that command.")

    return render(request, "alexa.html")

