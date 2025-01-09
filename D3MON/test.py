''' AI Mdoule is best module for begginer programmers who want to build their own personal assistant. '''
import datetime
import os
from re import search
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import bs4
from linksearch import *
import requests


class AI():
    ''' Engine Of AI Module'''

    def __init__(self, AiName: str = "jarvis", userGender: str = "male", Voice: int = 0):
        self.AiName = AiName
        self.userGender = userGender
        self.SM = "Sir"
        if self.userGender == "female":
            self.SM = "Mam"
        self.Voice = Voice
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        print(self.voices)
        self.engine.setProperty("voice", self.voices[self.Voice].id)

    '''It works like brain of the AI'''

    def Brain(self):
        PasswordList = [f"hey {self.AiName}", f"hi {self.AiName}", f"hello {self.AiName}",
                        f"{self.AiName} let's start work"]
        if self.TLoop(PasswordList):
            # self.wishMe()
            print("self.WishMe Just Run")
            while (True):
                # Query = self.TakeCommand().lower()
                Query = input("Enter the data: ")

                if f"{self.AiName} say" in Query:
                    '''It Return User's Sentences or do mimicry'''
                    Query = Query.replace(f"{self.AiName} say", "")
                    self.Speak(Query)

                elif f"{self.AiName} open youtube" in Query:
                    self.openWebsite("www.youtube.com")
                elif f"{self.AiName} open code" in Query:
                    self.openApp("C:\\Users\\saura\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

                elif self.AiName in Query and "open website" in Query:
                    '''It opens the website but it required the name of website.'''
                    '''
                        search: This method need query(website name) as a parameter and it return the website 
                                links related to query.
                        Query: Here query is a website name.
                        num_results: It get integer value and return the links. If it's value is 5 then 
                                     it return 5 links related to query. '''
                    print("Please tell me website name.")
                    self.Speak("Please tell me website name.")
                    # Query = self.TakeCommand().lower()
                    Query = input("Enter the data: ")
                    if Query:
                        linksearch(Query)
                elif self.AiName in Query and "relax" in Query:
                    '''It used for avoid the all queries until user speak right command for reverse the condition.'''
                    RelaxOperationList = [f"{self.AiName} wake up"]
                    if self.TLoop(RelaxOperationList):
                        print(f"I am ready to work with you {self.SM}.")
                        self.Speak(f"I am ready to work with you {self.SM}.")
                elif self.AiName in Query and "go to sleep" in Query:
                    '''It is used for stop the personal assistant.'''
                    break

    # --------------    I will be work on file related functions, watch the file_function.py file.    ---------- #

    def TLoop(self, ValueList: list):
        while (True):
            # Query = self.TakeCommand().lower()
            Query = input("Enter the data: ")
            if self.checkMultipleValues(Query, ValueList):
                return True
            else:
                pass

    ''' Speak function:
        audio: User's Input,
        Ex; audio(124421), audio("Hello Buddy"), audio(True)'''

    def Speak(self, audio):
        try:
            self.engine.say(audio)
            self.engine.runAndWait()
        except Exception as e:
            print(f"I can't speak. There are some techinical issue.")

    ''' TakeCommand function: Used for get command from user as a string'''

    def TakeCommand(self):
        self.Brain = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            self.audio = self.Brain.listen(source)
        try:
            print("Recognizing...")
            self.query = self.Brain.recognize_google(self.audio, language="en-in")
            print(f"Query: {self.query}\n")
            return self.query
        except Exception as e:
            print("Sir can you say again for me,Please\n")
            return self.TakeCommand()

    ''' WhishMe Function:
    List = User can use list for multiple wishes '''

    def wishMe(self, List: list = None):
        try:
            if List == None:
                List = ["how can i help you", "what can i do for you", "nice to meet you"]
            self.engine.setProperty("rate", 170)
            self.hour = int(datetime.datetime.now().hour)
            self.Wish = random.choice(List)
            if self.Wish == "how can i help you Sir":
                self.engine.setProperty("rate", 174)
            if self.hour >= 4 and self.hour < 12:
                Timewish = f"Good Morning {self.SM}"
                self.Speak(Timewish)
                self.Speak(self.Wish)
            elif self.hour >= 12 and self.hour < 18:
                Timewish = f"Good Afternoon {self.SM}"
                self.Speak(Timewish)
                self.Speak(self.Wish)
            elif self.hour >= 18 and self.hour < 20:
                Timewish = f"Good Evening {self.SM}"
                self.Speak(Timewish)
                self.Speak(self.Wish)
            elif (self.hour >= 20 and self.hour < 24) or (self.hour >= 0 and self.hour < 4):
                Timewish = f"Good Night {self.SM}"
                self.Speak(Timewish)
                self.Speak(self.Wish)
        except Exception as e:
            pass

    ''' Password Types '''
    ''' 1. Used For check query is available in given values,
    Return booelan value: True or False,
    query: User's Enter Data,
    List (List of values): It is required and used for store the values. '''

    def checkMultipleValues(self, query: str, List: list) -> bool:
        for i in List:
            if query == i:
                return True
        return False

    ''' 2. Used for check query and value is same or not,
    Return booelan value: True or False,
    query: User's Enter Data,
    svalue: User's predefined value (Supports string)'''

    def checkSingleValue(self, query: str, svalue: str) -> bool:
        if query == svalue:
            return True
        else:
            return False

    ''' Open websites and applications '''
    ''' 1. For Websites,
    url: Website url or link as a string,
    Ex; "https://www.google.com" '''

    def openWebsite(self, url: str):
        try:
            webbrowser.open(url)
        except Exception as e:
            pass

    ''' 2. For Applications,
    Set path for applicatiion,
    Ex: "D:\\Movies and web series" '''

    def openApp(self, path: str):
        try:
            os.startfile(path)
        except Exception as e:
            pass

    ''' File related operations '''
    ''' 1. For reading the file, 
    path: File path as a string '''

    def readFile(self, path: str):
        with open(path, "r") as file:
            return file.read()

    ''' 2. For writing the file, 
    path: File path as a string,
    content: It is the data which stored as a string in file '''

    def writeFile(self, path: str, content):
        with open(path, "w") as file:
            file.write(f"{content}")


def Trisha():
    AI(AiName="trisha", Voice=0).Brain()


if __name__ == "__main__":
    Trisha()