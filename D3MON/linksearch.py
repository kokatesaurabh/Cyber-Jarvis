from bs4 import BeautifulSoup
import requests
import webbrowser

class linksearch:
    def __init__(self,query):
        query = query.replace(" ","+")
        self.url = f"https://www.google.com/search?q={query}"
        self.search(self.url)

    def search(self,url):
        self.webpage = requests.get(url)
        self.webpagedata = BeautifulSoup(self.webpage.text,'html.parser')
        self.links = self.webpagedata.find_all('a')
        for index,link in enumerate(self.links):
            link = link.get('href')
            link = self.baseUrl(link)
            self.link = self.decodeLink(link)
            if 'https://www.' in self.link:
                link = link.replace('/url?q=',"")
                webbrowser.open(link)
                break

    def baseUrl(self,link:str):
        link_data = link.split("&")
        return link_data[0]

    def decodeLink(self,link:str):
        self.CharDict = {'%20': ' ','%21': '!','%22': '"','%23': '#','%24': '$','%26': '&','%27': '\'','%28': '(','%29': ')','%2A': '*','%2B': '+','%2C': ',','%2F': '/','%3A': ':','%3B': ';','%3D': '=','%3F': '?','%40': '@'}
        for i in self.CharDict:
            if i in link:
                link = link.replace(i,self.CharDict[i])
        return link

# linksearch("")