from applications.search import crawler
from datamodel.search import datamodel
from applications.search import crawler_frame
from urllib2 import urlopen, Request
import urlparse
from lxml import html, etree
from bs4 import BeautifulSoup
print("HELLO WELCOME TO THE MAIN FILE :D")

def linkRetrieve(url):
    links = []
    stripChars = "../"
    content = urlopen(url)
    htmlFile = content.read()
    soup = BeautifulSoup(htmlFile,"lxml")
    for item in soup.find_all('a'):
        foundUrl = item.get('href')
        if foundUrl != "/":
            if foundUrl[0:4] != "http" and foundUrl[0:3] != "www":
                links.append(urlparse.urljoin(url,foundUrl))
            else:
                links.append(item.get('href'))
    content.close()
    return links
    

if __name__=="__main__":
    url = "http://fano.ics.uci.edu/cites/"
    print(linkRetrieve(url))
    statement = crawler_frame.is_valid("https://duttgroup.ics.uci.edu?query=hello")
    print(statement)
    crawler.SetupLoggers()
    c = crawler.Simulation("amazon.ics.uci.edu",9050)
