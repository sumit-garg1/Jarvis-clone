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
    engine.setProperty("voice", voices[0])  # Using default voice (index 0)
    
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Ensure the event loop is stopped after speaking

def get_command():
    with sp.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            # Set timeout and phrase time limit for better performance
            audio = listener.listen(source, timeout=5, phrase_time_limit=10)  
            command = listener.recognize_google(audio, language="en-in")
            print(f"Recognized command: {command}")  # For debugging purposes
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
    # Only start listening when the form is submitted via POST request
    if request.method == 'POST':
        command = get_command()

        if command is None:  # If no command is recognized, continue listening
            return render(request, "alexa.html")

        if 'jarvis' in command:  # Trigger Alexa with the wake word 'Jarvis'
            command = command.replace('jarvis', '').strip()

            # Handle 'play' command
            if 'play' in command:
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

                # Open WhatsApp Web
                if 'whatsapp' in app:
                    speak("Opening WhatsApp")
                    webbrowser.open("https://web.whatsapp.com/")

                # Open desktop apps
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
                
                # Open the first search result using web browser
                result = next(search(query), None)
                if result:
                    webbrowser.open(result)
                else:
                    speak(f"Sorry, I couldn't find any information about {query}.")

            # If the command is not recognized
            else:
                speak("Sorry, I didn't understand that command.")

    # Render the page again after handling the command
    return render(request, "alexa.html")
