import logging
from datamodel.search.datamodel import ProducedLink, OneUnProcessedGroup, robot_manager, Link
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter
from lxml import html,etree
import re, os
from time import time
import codecs
from bs4 import BeautifulSoup

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


def read_previous_max_outlinks():
    directory = "analytics"
    filename = "outlink_max.txt"
    filepath = "{dir}/{filename}".format(dir=directory,filename=filename)
    count =0
    if os.path.exists(filepath):
        with codecs.open(filepath, 'r',encoding="utf-8") as f:
            line = f.readline()
            if line:
                count = line.split("::")[0]
    return count

def handle_subdomain(baseUrl):
    urlinfo = urlparse(baseUrl)
    subdomain = urlinfo.hostname.split('.')[0]
    directory = "analytics/subdomains"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = "{subdomain}.txt".format(subdomain = subdomain)
    filepath = "{dir}/{filename}".format(dir=directory,filename=filename)
    with codecs.open(filepath, 'a+',encoding="utf-8") as f:
        f.write(baseUrl+'\n')
    
def writeToFile(filename, content, mode):
    directory = "analytics"
    filePath = "{dir}/{filename}".format(dir=directory,filename=filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with codecs.open(filePath, mode,encoding="utf-8") as f:
        f.write(content)
    





@Producer(ProducedLink, Link)
@GetterSetter(OneUnProcessedGroup)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        # Set app_id <student_id1>_<student_id2>...
        self.app_id = "52192782_30392887_45754269"
        # Set user agent string to IR W17 UnderGrad <student_id1>, <student_id2> ...
        # If Graduate studetn, change the UnderGrad part to Grad.
        self.UserAgentString = "IR S17 UNDERGRAD 52192782, 30392887, 45754269"
		
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
def get_url_content(contentFile,baseUrl):
    '''
    Function returns a list, in links variable, of absolute url's from an HTML file provided by contentFile. The contentFile is associated 
    with the baseUrl that it is linked to. BeautifulSoup will take the HTML content and use lxml as its main parser, extract all link tags 
    and retrieve their url's from the href field. In this function it can be assumed baseUrl is valid and has content. Relative urls do not 
    begin the http, https, www, prefix. It is usually started with a word, / , or ../ so this can be checked through string slicing. If relative
    join it with the base url and add it to the list. If not the add it to the list as is.
    This function does not check if the url's are duplicates or have crawler or bot issues, this handled by frontier.
    '''
    filter_exp = "\.\."
    stripChars = "../"
    splitExceptions = ["/",""]
    links = []
    soup = BeautifulSoup(contentFile,"lxml")
    for item in soup.find_all('a'):
        foundUrl = item.get('href')
        if foundUrl and foundUrl != "" and foundUrl != "/":
    		if foundUrl[0:4] != "http" and foundUrl[0:3] != "www":
    			links.append(urljoin(baseUrl,foundUrl))
    		else:
    			links.append(foundUrl)
    return links
def extract_next_links(rawDatas):
    PREVIOUS_MAX_LINKS = read_previous_max_outlinks()
    outputLinks = list()
    for data in rawDatas:
        # http://www.restapitutorial.com/httpstatuscodes.html
        if data.http_code not in ["200", "301","302","307"]:
            data.bad_url = True
            writeToFile("invalid_links.txt","{link}::{code}\n".format(link=data.url, code=data.http_code), "a+")
        else:
            baseUrl = data.url
            if data.is_redirected == True:
                baseUrl = data.final_url
                # we do not need to put the base or final url back into the 
                # frontier.
                #outputLinks.append(data.final_url)
            otherLinks = get_url_content(data.content,baseUrl)
            if len(otherLinks)>PREVIOUS_MAX_LINKS:
                PREVIOUS_MAX_LINKS = len(otherLinks)
                writeToFile("outlink_max.txt", "{count}::{link}".format(count=PREVIOUS_MAX_LINKS, link=baseUrl), "w")
            outputLinks += otherLinks
            
            handle_subdomain(baseUrl)
            
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
    if (parsed.scheme not in set(["http", "https"])) or (url.find("?") != -1):
        return False
    crawler_traps = ['calendar.ics.uci.edu','archive.ics.uci.edu']
    if parsed.hostname in crawler_traps:
        return False
    # to remove the urls that are ridiculously long. 
    # 25 is an arbitrary number, we can change it to a more realistic number if needed.  
    parts = url.split("/")
    if len(parts) > 25:
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
