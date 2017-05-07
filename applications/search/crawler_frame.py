import logging
from datamodel.search.datamodel import ProducedLink, OneUnProcessedGroup, robot_manager, Link
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
from bs4 import BeautifulSoup
from datetime import datetime
## Above import is to make a unique log header for each file
try:
    # For python 2
    from urlparse import urlparse, parse_qs, urljoin
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs


logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"
url_count = (set() 
    if not os.path.exists("successful_urls.txt") else 
    set([line.strip() for line in open("successful_urls.txt").readlines() if line.strip() != ""]))
MAX_LINKS_TO_DOWNLOAD = 3000
TEST_DICT = {"PROMPT": "HI"} ## Was used for testing can be ommitted in final version
GLOBAL_DICT = {"subdomains":{".edu":0},"invalids":0,"redirects":0,"orig-relative":0} ##Nested dictionary structure that has information on the whole webCrawl
########################################################################################
###GLOBAL_DICT["subdomain"] contains an inner dictionary which will have the subdomain count of all domains i.e. .edu, .uci.edu, .ics.uci.edu, .fano.ics.uci.edu
###GLOBAL_DICT["orig-relative"] counts amount of relative-urls encountered that had to be reformatted as absolute, can be taken out in final version
URL_DICT = {}
##URL_DICT has all unique urls as keys and their number of outlinks as value i.e. (URL_DICT = {"fano.ics.uci.edu/graphs.html":34})
URL_INC = 0
URL_OUT_ACCUM = 0
@Producer(ProducedLink, Link)
@GetterSetter(OneUnProcessedGroup)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        # Set app_id <student_id1>_<student_id2>...
        self.app_id = "52192782_30392887_45754269"
        # Set user agent string to IR W17 UnderGrad <student_id1>, <student_id2> ...
        # If Graduate studetn, change the UnderGrad part to Grad.
        self.UserAgentString = "IR S17 UNDERGRAD 52192782 30392887 45754269"
        self.frame = frame
        assert(self.UserAgentString != None)
        assert(self.app_id != "")
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def initialize(self):
        self.count = 0
        l = ProducedLink("http://www.ics.uci.edu", self.UserAgentString)
        print l.full_url
        self.frame.add(l)

    def update(self):
        for g in self.frame.get_new(OneUnProcessedGroup):
            print "Got a Group"
            outputLinks, urlResps = process_url_group(g, self.UserAgentString)
            for urlResp in urlResps:
                if urlResp.bad_url and self.UserAgentString not in set(urlResp.dataframe_obj.bad_url):
                    urlResp.dataframe_obj.bad_url += [self.UserAgentString]
            for l in outputLinks:
                if is_valid(l) and robot_manager.Allowed(l, self.UserAgentString):
                    lObj = ProducedLink(l, self.UserAgentString)
                    self.frame.add(lObj)
        if len(url_count) >= MAX_LINKS_TO_DOWNLOAD:
            self.done = True

    def shutdown(self):
        print "downloaded ", len(url_count), " in ", time() - self.starttime, " seconds."
        pass

def save_count(urls):
    global url_count
    urls = set(urls).difference(url_count)
    url_count.update(urls)
    if len(urls):
        with open("successful_urls.txt", "a") as surls:
            surls.write(("\n". join(urls) + "\n").encode("utf-8"))

def process_url_group(group, useragentstr):
    rawDatas, successfull_urls = group.download(useragentstr, is_valid)
    save_count(successfull_urls)
    return extract_next_links(rawDatas), rawDatas
    
#######################################################################################
'''
STUB FUNCTIONS TO BE FILLED OUT BY THE STUDENT.
'''
def countDomains(domain):
    '''
    Count the amount of subdomains in a url String. A subdomain denoted by a "." in baseUrl
    '''
    count = 0
    for i in domain:
        if i == ".":
            count += 1
    return count
def rejoin(domainList):
    '''
    Take list of domains and recombine them into a string
    '''
    baseStr = ""
    for i in domainList:
        baseStr += i + "."
    baseStr = "." + baseStr
    return baseStr[0:len(baseStr) - 1]

def splitDomains(url):
    '''
    Get baseUrl from url string to find subdomains. Input is always an ABSOLUTE url
    '''
    baseUrl = url.split("/")[2].strip("www.") ###Separate directories and retrieve base url
    subdomains = baseUrl.split(".") ### Split into subdomain list
    indexList = []
    logtoDict(subdomains,global_dict) ### Use subdomain list to log to total count of all subdomains visited
    return baseUrl

def logtoDict(domainList,referenceDict):
    '''
    Used to log and count the frequency of each subdomain in a url during the whole web crawling process.
    Frequencies are added to referenceDict parameter
    '''
    end = len(domainList) ##Mark stopping point in recursively generating subdomains
    for i in range(end,-1,-1): ## For every subdomain token
        rejoined = rejoin(domainList[i : end]) ##Make a new concatenated subdomain string
        if rejoined != '': ##Filter out empty string
            if rejoined in referenceDict["subdomains"]: ##Increment subdomain frequency in the dictionary or add it to the diction in ["subdomains"] section
                referenceDict["subdomains"][rejoined] += 1
            else:
                referenceDict["subdomains"][rejoined] = 1
def prettyFormat(keyList):
    for i in keyList:
        domainStr = "Domain/Subdomain:  " + i[0]
        freq = "Frequency:  " + str(i[1])
        print("{0:<40} {1:>8}".format(domainStr,freq))
def checkforTrap(url):
    '''
    Checks for crawler traps in the url usually contained by having "/data/directory/data/directory/data/directory/data/directory/data/directory/"
    patterns that lead strange pages. True for if it has this pattern and is a likely trap, False if not.
    ''' 
    directories = filter(lambda item: item != '',url.split("/")) ##Split the url by directories
    original = len(directories) ## Count directories of original url
    filtered = len(set(directories)) ##Have a list of only the UNIQUE directories, many traps just infinitely copy the same directories in url
    if original - filtered > 4: ##Check difference between original list and filtered set.
        return True
    return False
def filterOutId(url):
    baseUrl = url
    idIndex = url.find("#")
    if idIndex != -1:
        return baseUrl[0:idIndex]
    return baseUrl
def filterCD(url):
    '''
    Filter out ../ string url string, the return string is a string that contains all of the url before the first "../" expression
    '''
    filter_exp = r'\.\./' 
    matchObj = re.search(filter_exp,url) ##Check if url has expression
    if matchObj == None: ##If not return original and do not modifiy
        return url
    else: ##If it does,  only return the part of the url UP TO that expression token.
        newUrl = url[0:matchObj.start()]
        return newUrl
def makeOutputFile(fileName,crawlerDict,outDict):
    '''
    Once all url's have been crawled. Use the global crawling dictionary and the url dictionary containing number of outlinks per url.
    Log all the information in a formatted manner to a file.
    '''
    current =  datetime.today() ## Get and log date and time of the web crawl 
    baseStr = "Making a crawler log on " + str(current.month) + " - " + str(current.day) + " - " + str(current.year) + " at Time " + str(current.hour) + " : " + str(current.minute) + " \n"
    baseStr += "Subdomain Logs\n" ##Display subdomain frequencies from the crawlerDict parameter
    for key in crawlerDict["subdomains"]:
        domainStr = "Domain/Subdomain: " + key
        frequency = "Frequency: " + str(crawlerDict["subdomains"][key])
        formatString = "{0:<40} {1:>8}".format(domainStr,frequency)
        baseStr += (formatString + "\n")
    baseStr += ("Total Redirects:  " + str(crawlerDict["redirects"]) + "\n") ##Log redirect count
    baseStr += ("Invalid URLs:  " + str(crawlerDict["invalid"]) + " in total.\n") ##Log invalid url count
    baseStr += ("Non-absolute Urls Crawled:  " + str(crawlerDict["orig-relative"]) + "\n") ##Log total relative-urls encountered
    listPairs = sorted(outDict.items(),key = lambda itm : (-1 * itm[1],itm[0]))
    baseStr += ("Top url is:  " + listPairs[0][0] + " at " + str(listPairs[0][1]) + " outlinks.\n") ## Log url with most outlinks
    log = open(fileName,"a") ##Open file for appending
    log.write(baseStr) ##Write all data
    log.close() ##Close file
def get_url_content(contentFile,baseUrl):
    '''
    Function returns a list, in links variable, of absolute url's from an HTML file provided by contentFile. The contentFile is associated 
    with the baseUrl that it is linked to. BeautifulSoup will take the HTML content and use lxml as its main parser, extract all link tags 
    and retrieve their url's from the href field. In this function it can be assumed baseUrl is valid and has content. Relative urls do not 
    begin the http, https, www, prefix. It is usually started with a word, / , or ../ so this can be checked through string slicing. If relative
    join it with the base url and add it to the list. If not the add it to the list as is.
    This function does not check if the url's are duplicates or have crawler or bot issues, this handled by frontier.
    '''
    filter_exp = '\.\./'
    stripChars = "../"
    splitExceptions = ["/",""]
    links = []
    soup = BeautifulSoup(contentFile,"lxml")
    for item in soup.find_all('a'):
        foundUrl = item.get('href')
        if foundUrl != "/":
            if foundUrl[0:4] != "http" and foundUrl[0:3] != "www":
                links.append(urljoin(baseUrl,foundUrl))
            else:
                links.append(item.get('href'))
####alternate body
##    soup = BeautifulSoup(contentFile,"lxml")
##    linkList = soup.find_all('a')
##    outCount = len(linkList)
##    if url not in URL_DICT:
##        URL_DICT[url] = outCount
##            foundUrl = filterCD(item.get('href')) ##f
##            if foundUrl != "/":
##            if foundUrl[0:4] != "http" and foundUrl[0:3] != "www":
##                links.append(urljoin(baseUrl,foundUrl))
##                GLOBAL_DICTS["orig-relative"] += 1
##            else:
##                links.append(foundUrl)      
    return links
def extract_next_links(rawDatas):
    TEST_DICT["PROMPT"] = "Hello"
    validStatusCodes = [200,301,302,307]
    outputLinks = list()
    for data in rawDatas:
        if data.http_code not in validStatusCodes:
            data.bad_url = True
            ##GLOBAL_DICT["invalid"] += 1 
        else:
            baseUrl = data.url
            if data.is_redirected == True:
                baseUrl = data.final_url
                ##GLOBAL_DICT["redirects"] += 1
            otherLinks = get_url_content(data.content,baseUrl)
            outputLinks += otherLinks
    '''
    rawDatas is a list of objs -> [raw_content_obj1, raw_content_obj2, ....]
    Each obj is of type UrlResponse  declared at L28-42 datamodel/search/datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.

    Suggested library: lxml
    '''
    return outputLinks

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be downloaded or not.
    Robot rules and duplication rules are checked separately.

    This is a great place to filter out crawler traps.
    '''
    queryChars = "[\?=+,]"
    parsed = urlparse(url)
    crawler_traps = ['calendar.ics.uci.edu','archive.ics.uci.edu']
    parts = url.split("/")
    if len(parts) >= 15: ##I have checked some of the traps this number should be shorter more like 11-15
        return False
##    if (parsed.scheme not in set(["http", "https"])) or (url.find("?") != -1) or (checkforTrap(url) == True) or (re.match("doku.php") == True:
##        return False
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
