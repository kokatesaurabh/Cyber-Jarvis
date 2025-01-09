''' VDesktopAssistant Mdoule is best module for begginer programmers who want to build their own personal desktop assistant. '''
import pyttsx3
import speech_recognition as sr
import requests
from bs4 import *
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

    ''' This functions provide help to get proper url.'''
    def baseUrl(self,url:str):
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

    def decodeUrl(self,url:str):
        for char in self.CharDict:
            if char in url:
                url = url.replace(char,self.CharDict[char])
        return url

class WebSearch(AssistFunc):
    def linkSearch(self,query:str,start:str=1,stop:str=1,safeSearch:bool=True):
        query = query.replace(" ","+")
        url = f"https://www.google.com/search?q={query}"
        try:
            webpage = requests.get(url)
        except Exception:
            print(Exception)
            return False
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
                    count = count + 1
                if count == stop:
                    break
        return linkList

    def YtSearch(self, query: str):
        query = query.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        return url

class WikiSearch:
    def __init__(self,wiki_link):
        self.wiki_link = wiki_link

    def paraSearch(self,para:int=1,skip:int=0):
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
        except Exception:
            print("May be your internet connection is off.")
            return False

class AI:
    ''' Engine Of Virtual Desktop Assistant Module'''
    def __init__(self,AiName:str="jarvis",userGender:str="male",Voice:int=0):
        self.AiName = AiName
        self.userGender = userGender
        self.SM = self.respect(userGender)
        self.Voice = Voice
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice",self.voices[self.Voice].id)
    '''It works like brain of the AI'''
    def Brain(self):
        # self.internetConnection()
        PasswordList = [f"hey {self.AiName}",f"hi {self.AiName}",f"hello {self.AiName}",f"{self.AiName} let's start work"]
        RelaxOperationList =[f"{self.AiName} wake up"]
        if self.TLoop(PasswordList):
            # self.wishMe()
            print(f"self.WishMe Just Run, Hello {self.SM}")
            # self.Speak(f"self.WishMe Just Run, Hello {self.SM}")
            while(True):
                # Query = self.TakeCommand().lower()
                Query = input("Enter the data: ")

                if f"{self.AiName} say" in Query:
                    '''It Return User's Sentences or do mimicry'''
                    Query = Query.replace(f"{self.AiName} say","")
                    self.Speak(Query)

                elif self.AiName in Query and "open" in Query and "website" in Query:
                    Query = Query.split(" ")
                    WebsiteNames = []
                    for index,word in enumerate(Query):
                        if word == "open" and (index+1) <= len(Query):
                            WebsiteNames.append(Query[index+1])
                    print(WebsiteNames)
                    WebsiteList = self.findWebsites(WebsiteNames)
                    print(WebsiteList)
                    for website in WebsiteList:
                        webbrowser.open(website[0])
                    # if user use 'and' then also this function access website name , make it like that.

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
                        print("Wikipedia don't have any information about target.\n")
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
                    '''It used for avoid the all queries until user speak right command for reverse the condition.'''
                    if self.TLoop(RelaxOperationList):
                        print(f"I am ready to work with you {self.SM}.")
                        self.Speak(f"I am ready to work with you {self.SM}.")
                elif self.AiName in Query and "go to sleep" in Query:
                    '''It is used for stop the personal assistant.'''
                    break

    def respect(self,gender):
        if gender == "male":
            return "Sir"
        elif gender == "female":
            return "Mam"
        else:
            print("Please Mention your gender correctly.")
            return ""

    def internetConnection(self):
        try:
            if socket.create_connection(("8.8.8.8",53),timeout=1):
                return True
        except Exception:
            print("Please Check Your Internet Connection.")
            time.sleep(2)
            return self.internetConnection()

    def TLoop(self,ValueList:list):
        while(True):
            # Query = self.TakeCommand().lower()
            Query = input("Enter the data: ")
            if self.checkMultipleValues(Query,ValueList):
                return True
            else:
                pass

    def Speak(self,audio):
        '''
        Speak function gives any value as input and return audio.
        Ex; Speak(124421), Speak("Hello Buddy"), Speak(True)

        audio: User's Input.
        '''
        try:
            self.engine.say(audio)
            self.engine.runAndWait()
        except Exception as e:
            print(f"I can't speak. There are some techinical issue.")

    ''' TakeCommand function: Used for get command from user as a string'''
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
        except requests.exceptions.ConnectionError:
            print(f"{self.SM}, Please check your internet connection")
        except Exception as e:
            print(f"{self.SM} can you say again for me,Please\n")
            return self.TakeCommand()

#   I Want to update wishMe function in future.
    ''' WhishMe Function:
    List = User can use list for multiple wishes '''
    def wishMe(self, List:list=None):
        try:
            if List==None:
                List = ["how can i help you","what can i do for you","nice to meet you"]
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
            elif (self.hour >= 20 and self.hour < 24) or (self.hour >= 0 and self.hour <4):
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
    def checkMultipleValues(self,query:str,List:list) -> bool:
        for i in List:
            if query == i:
                return True
        return False
    ''' 2. Used for check query and value is same or not,
    Return booelan value: True or False,
    query: User's Enter Data,
    svalue: User's predefined value (Supports string)'''
    def checkSingleValue(self,query:str,svalue:str) -> bool:
        if query == svalue:
            return True
        else:
            return False

    ''' Open websites and applications '''
    ''' 1. For Websites,
    url: Website url or link as a string,
    Ex; "https://www.google.com" '''
    def openWebsite(self,url:str):
        try:
            webbrowser.open(url)
        except Exception as e:
            pass

    def openWebsites(self,li:list,open_link:int=1):
        if len(li) >= open_link:
            for i in range(open_link):
                webbrowser.open(li[i])
        else:
            return self.openWebsites(li,open_link=1)

    def findWebsites(self,li:list,start:str=1,stop:int=1,safeSearch:bool=True):
            '''
            find_link: it returns specified number of links.
            '''
            websiteList = []
            for webname in li:
                linksList = WebSearch().linkSearch(webname,start,stop,safeSearch)
                if linksList:
                    websiteList.append(linksList)
            return websiteList

    ''' 2. For Applications,
    Set path for applicatiion,
    Ex: "D:\\Movies and web series" '''
    def openApp(self,path:str):
        try:
            os.startfile(path)
        except Exception as e:
            pass

    ''' File related operations '''
    ''' 1. For reading the file, 
    path: File path as a string '''
    def readFile(self,path:str):
        with open(path,"r") as file:
            Data = file.read()
        return Data
    ''' 2. For writing the file, 
    path: File path as a string,
    content: It is the data which stored as a string in file '''
    def writeFile(self,path:str,content:str):
        with open(path,"w") as file:
            file.write(content)

def Trisha():
    Trisha = AI(AiName="trisha",Voice=2)
    Trisha.Brain()

if __name__ == "__main__":    
    Trisha()