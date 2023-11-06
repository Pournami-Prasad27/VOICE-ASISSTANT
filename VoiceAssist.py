from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.app import Builder
from kivy.core.window import Window
import speech_recognition as sr
from kivymd.uix.screenmanager import ScreenManager
import threading
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import webbrowser



KV = '''
ScreenManager:
    MenuScreen:
    AssistantScreen:

<MenuScreen>:
    name: 'menu'
    MDFlatButton:
        text: 'Call voice assistant'
        size_hint : (1,1)
        font_style:"H4"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press: root.manager.current = 'assistant'
    
    MDLabel:
        text: 'Connect Your Headphones Before Continuing'
        size_hint : (1,1)
        halign: 'center'
        font_style:"H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        

    MDFloatingActionButton:
        icon: "microphone"
        icon_color:"black"
        font_size:45
        on_press: root.manager.current = 'assistant'
        elevation_normal: 12
        pos_hint: {'x': .475, 'y':.2}

<AssistantScreen>:
    name: 'assistant'

    MDFloatLayout:

        MDIcon:
            icon:'robot-love'
            font_size:150
            id: icon_label
            halign:'center'
            pos_hint: {'center_x':0.5,'center_y':0.7}
            theme_text_color: 'Custom'
            text_color:app.theme_cls.primary_color

        MDLabel:
            id: response_label
            text: 'Voice assistant response will appear here'          
            halign: 'center'
            markup: True
            font_style:"H5"           
            pos_hint: {'center_x':0.5,'center_y':0.45}

        MDLabel:
            id: status_label
            text: ''          
            halign: 'center'
            markup: True
            font_style:"H4"           
            pos_hint: {'center_x':0.5,'center_y':0.85}


        MDRaisedButton:
            text: 'Back to menu'
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}

            on_press: root.manager.current = 'menu'
'''


class MyVoiceAssistant(threading.Thread):
    def __init__(self, label, labelstat, iclabel):
        threading.Thread.__init__(self)
        self.messagelabel = label
        self.statuslabel = labelstat
        self.iconlabel = iclabel
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        female_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        self.engine.setProperty('voice', female_voice_id)
        self.engine.setProperty('voices', voices[1].id)
        self.r = sr.Recognizer()
        self.mic = sr.Microphone(device_index=1)
        self.conversation = ""
        self.user_name = "Nishant"
        self.bot_name = "Robert"
        self.last_command = ""


    def run(self):

        # Define a function for speaking text
        def speak(text):
            self.statuslabel.text = "speaking..."
            self.iconlabel.icon = "robot-excited"
            self.messagelabel.text = text
            self.engine.say(text)
            self.engine.runAndWait()

        # Define a function for getting the user's name
        def say_hello():
            speak("Hello, I am your personal assistant.")
            return

        # Define a function for getting the current time
        def get_time():
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {time}.")

        # Define a function for playing a song on YouTube
        def play_song(song_name):
            speak(f"Playing {song_name} on YouTube.")
            pywhatkit.playonyt(song_name)

        # Define a function for searching Webbrowser
        def whatsapp():
            speak("opening whatsaap for you\n")
            webbrowser.open("https://web.whatsapp.com/")

        # Define a function for telling a joke
        def tell_joke():
            joke = pyjokes.get_joke()
            speak(joke)

        def listening():
            self.statuslabel.text = "Listening..."
            self.iconlabel.icon = "robot-happy"

        def notlistening():
            self.statuslabel.text = "no longer listening"
            self.iconlabel.icon = "robot-dead"

        def takeCommand():
            while True:
                # Listen for audio input from the user
                with self.mic as source:
                    print("\n Listening...")
                    listening()

                    self.r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.r.listen(source)
                print("no longer listening")
                notlistening()

                # Try to recognize the user's command
                try:
                    command = self.r.recognize_google(audio)
                    print(f"User said: {command}")
                    break

                except:
                    speak("please say it")
                    continue
            return command


        # Define a loop to listen for commands and execute them
        def first():
            print("started")


            say_hello()

            while True:
                # Listen for audio input from the user
                with self.mic as source:
                    print("\n Listening...")
                    listening()

                    self.r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = self.r.listen(source)
                print("no longer listening")
                notlistening()

                # Try to recognize the user's command
                try:
                    command = self.r.recognize_google(audio)
                    print(f"User said: {command}")


                    # Execute the appropriate command function
                    if "time" in command:
                        get_time()

                    elif "take notes" in command:
                        speak("What should i write")
                        note = takeCommand()
                        try:
                            with open('Notes.txt', 'a') as file:
                                file.write(note+'\n')
                        except IOError as e:
                            print(f"Error: {e}")
                        speak("notes taken")

                    elif "read notes" in command:
                        speak("Reading Notes")
                        try:
                            with open('Notes.txt', 'r') as file:
                                reading = file.read()
                                if reading == "":
                                    speak("Notes is empty")
                                else:
                                    print("file reading " + reading)
                                    speak(reading)
                        except:
                            speak("Error occured")


                    elif "delete notes" in command:
                        try:
                            with open('Notes.txt', 'w') as file:
                                speak("Notes deleted")
                        except:
                            speak("Error")


                    elif "where is" in command:
                        command = command.replace("where is", "")
                        location = command
                        speak("User asked to Locate")
                        speak(location)
                        webbrowser.open("https://www.google.com/maps/search/" + location + "")


                    elif "play" in command:
                        song_name = command.replace("play", "")
                        play_song(song_name)

                    elif "search" in command:
                        query=command.replace("search","")
                        search_url = f"https://www.google.com/search?q={query}"
                        webbrowser.open_new_tab(search_url)
                        speak("web browser opening")
                        self.engine.runAndWait()


                    elif 'whatsapp' in command:
                         whatsapp()


                    elif "joke" in command:
                        tell_joke()

                    elif "goodbye" in command:
                        speak("Goodbye!")
                        break
                    else:
                        speak("Sorry, I cannot perform this task. I can Search, Play videos, Crack a joke, Tell time, as well as Take, Delete, Read notes")
                        continue
                except:
                    speak("Sorry, I didn't hear what you said. Please try again.")
                    continue

            return

        first()


class MenuScreen(Screen):
    pass


class AssistantScreen(Screen):
    def on_enter(self):
        self.ids.response_label.text = 'Voice assistant is listening...'
        voice_assistant = MyVoiceAssistant(self.ids.response_label, self.ids.status_label, self.ids.icon_label)
        voice_assistant.start()


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(AssistantScreen(name='assistant'))


class VoiceAssistantApp(MDApp):
    def build(self):
        Window.size = (1280, 720)
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Teal"

        return Builder.load_string(KV)


if __name__ == '__main__':
    VoiceAssistantApp().run()
