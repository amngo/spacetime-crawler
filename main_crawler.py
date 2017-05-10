from applications.search import crawler
from datamodel.search import datamodel
from applications.search import crawler_frame
from urllib2 import urlopen, Request
from lxml import html, etree
from bs4 import BeautifulSoup
import urlparse
import re
print("HELLO WELCOME TO THE MAIN FILE :D")


def is_valid_copy(url):
    '''
    Function returns True or False based on whether the url has to be downloaded or not.
    Robot rules and duplication rules are checked separately.

    This is a great place to filter out crawler traps.
    '''
    queryChars = "[\?=+,]"
    parsed = urlparse.urlparse(url)
    if (parsed.scheme not in set(["http", "https"])) or (url.find("?") != -1):
        return False
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    
    except TypeError:
        print ("TypeError for ", parsed)
    
def linkRetrieve(url):
    links = []
    stripChars = "../"
    content = urlopen(url)
    htmlFile = content.read()
    soup = BeautifulSoup(htmlFile,"lxml")
    linkList = soup.find_all('a')
    baseOutLinks = len(linkList)
    for item in linkList:
        foundUrl = item.get('href')
        if foundUrl != "/":
            if foundUrl[0:4] != "http" and foundUrl[0:3] != "www":
                foundUrl = urlparse.urljoin(url,foundUrl)
        idIndex = foundUrl.find("#")
        if idIndex != -1:
            foundUrl = foundUrl[0:idIndex]
        if is_valid_copy(foundUrl) == True:
            links.append(foundUrl)
    content.close()
    validOutLinks = len(links)
    print("There were a total of " + str(baseOutLinks) + " offered!")
    print("In total: " + str(validOutLinks) + " were valid!")
    return links

class CopyData:
    def __init__(self,urlString,code,finalString,isRedirect):
        self.url = urlString
        self.http_code = code
        self.final_url = finalString
        self.isBad = False
        self.is_redirected = isRedirect
        self.content = self.initializeHTML(self.url)
    def initializeHTML(self,urlString):
        urlObj = urlopen(urlString)
        urlFile = urlObj.read()
        urlObj.close()
        return urlFile
def makeRawObjects(fileLines):
    objList = []
    for i in range(0,len(fileLines)):
        if i % 50 == 0:
            newObj = CopyData(fileLines[i],404,"",False)
            objList.append(newObj)
        if i % 75 == 0 and i % 50 != 0:
            newObj = CopyData(fileLines[i],200,"http://fano.ics.uci.edu/cites/",True)
            objList.append(newObj)
        else:
            newObj = CopyData(fileLines[i],200,"",False)
            objList.append(newObj)
    return objList

if __name__=="__main__":
    print("Logger Testing")
##    print(crawler_frame.checkforTrap("http://www.ics.uci.edu/~mlearn/datasets/datasets/datasets/datasets/datasets/datasets/datasets/index.html"))
##    print(crawler_frame.checkforTrap("http://www.ics.uci.edu/grad/policies/GradPolicies_GradStudentReview.php/faculty/about/equity/computing/admissions/Prospective_ApplicationProcess.php"))
##    logFile = open("newFile.txt","a")
    url = "http://fano.ics.uci.edu/cites/"
    url2 = "http://fano.ics.uci.edu/cites/Publication/"
    redirect = "http://www.doorway.com"
    url3 = "http://www.ics.uci.edu/dept/"
    dataObj1 = CopyData(url,200,"",False)
    dataObj2 = CopyData(url2,200,"nope",False)
    dataObj3 = CopyData(redirect,200,url3,True)
##    print(linkRetrieve(url3))
##    logFile.close()
##    baseContent = urlopen(url3)
##    baseFile = baseContent.read()
##    print(crawler_frame.get_url_content(baseFile,url3))
##    baseContent.close()
##    print("DELIMITER!!!!\n\n\n\n\n\n\n")
    crawler_frame.extract_next_links([dataObj1,dataObj2,dataObj3])
    statement = crawler_frame.is_valid("https://duttgroup.ics.uci.edu?query=hello")
    print(statement)
##    crawler.SetupLoggers()
##    c = crawler.Simulation("amazon.ics.uci.edu",9050)
    urlFile = open("../successful_urls.txt","r")
    urlList = urlFile.readlines()
    print("Total URLs is " + str(len(urlList)))
    urlFile.close()
    for i in urlList:
        crawler_frame.analytics.splitDomains(i)
    print(crawler_frame.analytics.mainDict)
    print(crawler_frame.analytics.domains)
    print(crawler_frame.analytics.maxUrl)
    print(crawler_frame.analytics.MAXCOUNT)
    print(crawler_frame.RETRIEVE_COUNTER)
    crawler_frame.makeOutputFile("sampleAnalytics.txt",crawler_frame.analytics)

##Sample output on all links in successful_urls.txt
##HELLO WELCOME TO THE MAIN FILE :D
##Logger Testing
##False
##Total URLs is 742
##{'invalids': 0, 'orig-relative': 2446, 'redirects': 1}
##{'.ics.uci.edu': 745, '.uci.edu': 745, '.edu': 745, '.fano.ics.uci.edu': 2}
##http://fano.ics.uci.edu/cites/Publication/
##2407
##3
##Making a crawler log on 5 - 10 - 2017 at Time 13 : 47 
##Subdomain Logs
##Domain/Subdomain: .ics.uci.edu           Frequency: 745
##Domain/Subdomain: .uci.edu               Frequency: 745
##Domain/Subdomain: .edu                   Frequency: 745
##Domain/Subdomain: .fano.ics.uci.edu      Frequency: 2
##Total Redirects:  1
##Invalid URLs:  0 in total.
##Non-absolute Urls Crawled:  2446
##Top url is:  http://fano.ics.uci.edu/cites/Publication/ at 2407 outlinks.

    
    
