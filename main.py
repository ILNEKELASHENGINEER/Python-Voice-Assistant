import pyttsx3
import wolframalpha
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import sys
import ctypes
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from first import Ui_Dialog
from pymongo import MongoClient
from datetime import *

newq = ""
try:
    client = MongoClient()
    db = client.voice_history
except:
    print("Connect not completed")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# for inserting
def send(chat, res):
    today = date.today()
    d4 = today.strftime("%d-%b-%Y")
    t = datetime.today().strftime("%I:%M %p")
    chat = {"Chat": chat, "Response": res, "date": str(d4), "time": str(t)}
    collection = db.Chathistory
    collection.insert_one(chat)
    # pprint.pprint(collection.find_one())
    print("Data recorded in the database")


# for retriving
def ret():
    dab = client["voice_history"]
    col = dab["Chathistory"]
    x = col.find({}, {"Chat": 1, "Response": 1, "date": 1, "time": 1})
    for data in x:
        print(data)


# for deleting
def delete():
    dab = client["voice_history"]
    col = dab["Chathistory"]
    result = col.delete_many({})
    print("Successfully data cleared")


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self)
        super().__init__()

    def run(self):
        self.commands()

    def commands(self):
        speak("speak now. Im Listening")
        while True:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 0.5
                audio = r.listen(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                newq = query.lower()
                print(f"Your said: {query}\n")
                # wishme()

                if "show the chat history" in newq:
                    res = "Retrieving the chat history from database"
                    speak(res)
                    send(newq, res)
                    ret()
                elif ("clear the chat history" in newq) or ("delete the history" in newq):
                    res = "Clearing all the Chat history from the database."
                    x = "history cleared"
                    speak(res + " " + x)
                    send(newq, res)
                    delete()

                elif "how are you" in newq:
                    speak("Im fine!")
                    speak("What about you buddy")
                    res = "Im fine! What about you buddy"
                    send(newq, res)
                elif ("time now" in newq) or ("what's the time now" in newq):
                    t = datetime.today().strftime("%I:%M %p")
                    speak(str(t))
                    send(newq, t)
                    break
                elif "head of the department of cse" in newq or "hod of cse" in newq:
                    res = "Doctor N. shaanthi is currently a head of the department of computer science and engineering department"
                    speak(res)
                    send(newq, res)
                    break
                elif "how can i reach library" in newq or "how can i reach I T park library" in newq:
                    res = "oh that sounds interesting. Its very easy to reach library where ever you are in I T Park just take middle step from the entrance or get near to the deparment office" \
                          "then the library is pretty much closer to the department office"
                    speak(res)
                    send(newq,res)
                    break
                elif "how many seminar halls" in newq or "how many seminar halls are there in I T park" in newq:
                    res = "There are two seminar halls present in the I T Park both of them present in the T B I area"
                    speak(res)
                    send(newq,res)
                    break

                elif "computer center in" in newq or "ccs " in newq:
                    res = "there are 6 ccs in I. T park in the 1st floor."
                    speak(res)
                    send(newq, res)
                    break
                elif "Wi-Fi registration" in newq or "wifi in I T park" in newq:
                    res = "in the lunch area , nearer to the C S E office department after 4 15 everyday"
                    speak(res)
                    send(newq, res)
                    break
                elif "yoga hall in I T park" in newq or "yoga hall" in newq:
                    res = "straight up to the second floor"
                    speak(res)
                    send(newq, res)
                    break
                elif ("lock my pc" in newq) or ("lock my screen" in newq) or ("lock the screen" in newq) or (
                        "screen lock" in newq):
                    res = "screen locking in seconds"
                    speak(res)
                    send(newq, res)
                    ctypes.windll.user32.LockWorkStation()
                    break
                elif "who made you" in newq or "who build you" in newq or "who are you" in newq:
                    x = "Im a Advance Artificial Intelligence made using python. I was developed by nekelash, malar, " \
                        "kiru thiya sri "
                    res = x
                    speak(x)
                    break
                elif ('netflix' or 'net flix') in newq:
                    webbrowser.open_new_tab("https://www.netflix.com/in/")
                    res = "Opening net-flix on browser"
                    speak(res)
                    speak("Enter  your  email  address  and  get  started  with  your  popcorn's")
                    send(newq, res)
                    break
                elif 'open youtube' in newq:
                    webbrowser.open_new_tab("https://www.youtube.com/")
                    res = "Opening Youtube"
                    speak(res)
                    break
                elif ('google' or 'search in google') in newq:
                    if ('google' in newq) and ("search" not in newq):
                        a3 = newq.replace('google', '')
                        webbrowser.open_new_tab(a3)
                        res = "results for " + a3
                        send(newq, res)
                        break
                    else:
                        a3 = newq.replace('search in google', '')
                        webbrowser.open_new_tab(a3)
                        res = "results for " + a3
                        send(newq, res)
                        break
                elif 'wikipedia' in newq:
                    query = newq.replace('search in wikipedia', '')
                    try:
                        app_id = "nekelashil.21cse@kongu.edu"
                        cli = wolframalpha.Client(app_id)
                        res = cli.query(query)
                        answer = next(res.results).text
                        print(answer)
                        speak("Your answer is " + answer)
                        break
                    except:
                        query = query.split(' ')
                        query = " ".join(query[0:])

                        speak("I am searching for " + query)
                        print(wikipedia.summary(query, sentences=2))
                        res = wikipedia.summary(query,
                                                sentences=2)
                        speak(res)
                    send(query, res)
                    break

                if 'exit' in newq:
                    speak("THANK YOU FOR USING ME AND IM VERY GRATEFUL FOR YOU")
                    speak("Now you can press the Stop button in the right bottom corner to close the AI")
                    res = "Chat ended with exit statement"
                    send(newq, res)
                    break
                if len(newq) > 0:
                    send(newq, res)


            except Exception as e:
                print(e)
                print("Unable to Recognize your voice.")
                speak("Unable to Recognize your voice! speak again!")
                break


start = MainThread()


class Main(QMainWindow):
    count = 1
    hello = MainThread()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton1.clicked.connect(self.starttask)
        self.ui.Quit.clicked.connect(self.close)

    def starttask(self):
        if (self.count == 1):
            welcome = "Hai there"
            speak(welcome)
            self.count += 1
        self.ui.movie = QtGui.QMovie("voice_gif.gif")
        self.ui.gif.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.hello.commands()


app = QApplication(sys.argv)
neke = Main()
neke.show()
exit(app.exec_())
