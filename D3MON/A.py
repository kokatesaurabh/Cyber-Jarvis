import pyttsx3
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
import os
import socket
import datetime
import time
import random

class AssistFunc:
    def __init__(self):
        self.CharDict = {'%20': ' ','%21': '!','%22': '"','%23': '#','%24': '$','%26': '&','%27': '\'','%28': '(','%29': ')','%2A': '*','%2B': '+','%2C': ',','%2F': '/','%3A': ':','%3B': ';','%3D': '=','%3F': '?','%40': '@'}
        self.WrongLinks = ["https://www.google.com/preferences?hl=en"]

    def baseUrl(self, url):
        link = url.split("&")
        if 'http://' in link[0] or 'https://' in link[0]:
            link = link[0]
        elif 'http://' in link[1] or 'https://' in link[1]:
            link = link[1]
        else:
            link = "https://www.google.com"
            return link
        if "https://" in link:
            link = link.split("https://")[1]
            return f"https://{link}"
        elif "http://" in link:
            link = link.split("http://")[1]
            return f"http://{link}"
        return link

    def decodeUrl(self, url):
        for char in self.CharDict:
            if char in url:
                url = url.replace(char, self.CharDict[char])
        return url

class WebSearch(AssistFunc):
    def linkSearch(self, query, start=1, stop=1, safeSearch=True):
        query = query.replace(" ","+")
        url = f"https://www.google.com/search?q={query}"
        try:
            webpage = requests.get(url)
            webdata = BeautifulSoup(webpage.text,'html.parser')
            links = webdata.find_all('a')
            start -= 2
            count = -1
            linkList = []
            for link in links:
                execution = False
                link = link.get('href')
                if safeSearch:
                    if 'https://' in link:
                        execution = True
                else:
                    if 'http://' in link or 'https://' in link:
                        execution = True
                if execution:
                    if count > start:
                        link = self.decodeUrl(link)
                        link = self.baseUrl(link)
                        if link in self.WrongLinks:
                            continue
                        if link not in linkList:
                            linkList.append(link)
                        else:
                            execution = False
                    if execution:
                        count += 1
                    if count == stop:
                        break
            return linkList
        except Exception as e:
            print(e)
            return False

class WikiSearch:
    def __init__(self, wiki_link):
        self.wiki_link = wiki_link

    def paraSearch(self, para=1, skip=0):
        if "https://en.wikipedia.org/wiki/" not in self.wiki_link:
            return False
        try:
            web_page = requests.get(self.wiki_link)
            web_data = BeautifulSoup(web_page.text,'html.parser')
            div_tag = web_data.find('div', class_='mw-content-ltr mw-parser-output')
            p_tags = div_tag.find_all('p')
            if para == -1:
                para = True
            else:
                para += skip
            data = ''
            index = 0
            for p in p_tags:
                if index == para:
                    break
                if p.get_text(strip=True) and not p.find_parent('table'):
                    if index > skip:
                        data += p.get_text()
                    else:
                        data = p.get_text()
                    index += 1
            return data
        except Exception as e:
            print("May be your internet connection is off.")
            return False

class AI:
    def __init__(self, AiName="jarvis", userGender="male", Voice=0):
        self.AiName = AiName
        self.userGender = userGender
        self.SM = self.respect(userGender)
        self.Voice = Voice
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        if 0 <= self.Voice < len(self.voices):
            self.engine.setProperty("voice", self.voices[self.Voice].id)
        else:
            print("Voice index out of range. Using default voice.")
        self.engine.setProperty("rate", 150)

    def respect(self, gender):
        if gender == "male":
            return "Sir"
        elif gender == "female":
            return "Mam"
        else:
            print("Please mention your gender correctly.")
            return ""

    def internetConnection(self):
        try:
            if socket.create_connection(("8.8.8.8",53),timeout=1):
                return True
        except Exception as e:
            print("Please check your internet connection.")
            time.sleep(2)
            return self.internetConnection()

    def TakeCommand(self):
        self.Ear = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            self.audio = self.Ear.listen(source)
        try:
            print("Recognizing...")
            self.query = self.Ear.recognize_google(self.audio,language="en-in")
            print(f"Query: {self.query}\n")
            return self.query
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except sr.UnknownValueError:
            print("Sorry, I did not get that. Please try again.")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def Brain(self):
        PasswordList = [f"hey {self.AiName}",f"hi {self.AiName}",f"hello {self.AiName}",f"{self.AiName} let's start work"]
        RelaxOperationList = [f"{self.AiName} wake up"]
        if self.TLoop(PasswordList):
            print(f"Hello {self.SM}, how can I assist you?")
            while True:
                Query = self.TakeCommand().lower()

                if f"{self.AiName} say" in Query:
                    Query = Query.replace(f"{self.AiName} say","")
                    self.Speak(Query)

                elif self.AiName in Query and "open" in Query and "website" in Query:
                    Query = Query.split(" ")
                    WebsiteNames = [Query[index+1] for index,word in enumerate(Query) if word == "open" and (index+1) < len(Query)]
                    WebsiteList = self.findWebsites(WebsiteNames)
                    for website in WebsiteList:
                        webbrowser.open(website)

                elif f"{self.AiName} find information about" in Query:
                    Query = Query.replace(f"{self.AiName} find information about ","")
                    print(f"-----Target--{Query}-----\n")
                    Searches = [f"{Query} wikipedia",f"{Query} youtube video",f"{Query} facebook",f"{Query} instagram",f"{Query} twitter"]
                    links_list = self.findWebsites(Searches)
                    wikipedia_info = WikiSearch(links_list[0][0]).paraSearch(para=1)
                    if wikipedia_info:
                        print("Wikipedia Information:")
                        print(wikipedia_info)
                    else:
                        print("Wikipedia doesn't have any information about the target.\n")
                    print("Links: ")
                    print(f"Wikipedia: {links_list[0][0]}")
                    print(f"Youtube: {links_list[1][0]}")
                    print(f"Facebook: {links_list[2][0]}")
                    print(f"Instagram: {links_list[3][0]}")
                    print(f"Twitter: {links_list[4][0]}")
                    index = 0
                    for web_links in links_list:
                        if index > 0:
                            self.openWebsite(web_links[0])
                        index += 1

                elif self.AiName in Query and "relax" in Query:
                    if self.TLoop(RelaxOperationList):
                        print(f"I am ready to work with you {self.SM}.")
                        self.Speak(f"I am ready to work with you {self.SM}.")

                elif self.AiName in Query and "go to sleep" in Query:
                    print("Going to sleep...")
                    break

    def TLoop(self, ValueList):
        while True:
            Query = self.TakeCommand().lower()
            if self.checkMultipleValues(Query, ValueList):
                return True
            else:
                pass

    def Speak(self, audio):
        try:
            self.engine.say(audio)
            self.engine.runAndWait()
        except Exception as e:
            print("I can't speak. There are some technical issues.")

    def wishMe(self, List=None):
        try:
            if List == None:
                List = ["how can I help you","what can I do for you","nice to meet you"]
            self.hour = datetime.datetime.now().hour
            self.Wish = random.choice(List)
            if self.Wish == "how can I help you Sir":
                self.engine.setProperty("rate", 174)
            if 4 <= self.hour < 12:
                Timewish = f"Good Morning {self.SM}"
            elif 12 <= self.hour < 18:
                Timewish = f"Good Afternoon {self.SM}"
            elif 18 <= self.hour < 20:
                Timewish = f"Good Evening {self.SM}"
            else:
                Timewish = f"Good Night {self.SM}"
            self.Speak(Timewish)
            self.Speak(self.Wish)
        except Exception as e:
            print(f"Error in wishMe function: {e}")

    def checkMultipleValues(self, query, List):
        for i in List:
            if query == i:
                return True
        return False

    def openWebsite(self, url):
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening website: {e}")

    def findWebsites(self, li):
        websiteList = []
        for webname in li:
            linksList = WebSearch().linkSearch(webname)
            if linksList:
                websiteList.append(linksList[0])
        return websiteList

def D3mon():
    D3mon = AI(AiName="D3mon", Voice=2)
    D3mon.Brain()

if __name__ == "__main__":
    D3mon()