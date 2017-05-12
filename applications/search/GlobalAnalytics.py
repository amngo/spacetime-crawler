GLOBAL_DICT = {"invalids":0,"redirects":0,"orig-relative":0}
SUBDOMAINS = {".edu":0,".uci.edu":0,".ics.uci.edu":0}
COUNTER = {"url":"","count":0}
MAXCOUNT = 0
## Team information CS121: IR; Undergraduates; Spring 2017
## Joshua Pascascio, jpascasc@uci.edu, ID: 52192782
## Miguel Tolosa , tolosam@uci.edu, ID: 30392887
## Chang Shin Lee , changsl3@uci.edu, ID: 45754269
def countDomains(domain):
    '''
    Count the amount of subdomains in a url String. A subdomain denoted by a "." in baseUrl
    '''
    count = 0
    for i in domain:
        if i == ".":
            count += 1
    return count  

class AnalyticsObject:
    def __init__(self):
        self.mainDict = {"invalids":0,"redirects":0,"orig-relative":0}
        self.domains  = {".edu":0,".uci.edu":0,".ics.uci.edu":0}
        self.maxUrl = ""
        self.MAXCOUNT = 0
    def incrementInvalids(self):
        self.mainDict["invalids"] += 1
    def incrementResets(self):
        self.mainDict["redirects"] += 1
    def incrementRel(self):
        self.mainDict["orig-relative"] += 1
    def getCount(self):
        return self.MAXCOUNT
    def setMax(self,url,count):
        self.maxUrl = url
        self.MAXCOUNT = count
    def rejoin(self,domainList):
        baseStr = ""
        for i in domainList:
            baseStr += (i + ".")
        baseStr = "." + baseStr
        answer = baseStr[0:(len(baseStr) - 1)]
        return answer
    def splitDomains(self,url):
        baseUrl = url.split("/")[2].strip("www.") ###Separate directories and retrieve base url
        subdomains = baseUrl.split(".") ### Split into subdomain list
        self.logtoDict(subdomains) ### Use subdomain list to log to total count of all subdomains visited
    def resetUrl(self,url,count):
        if count > self.MAXCOUNT:
            self.maxUrl = url
            self.MAXCOUNT = count
    def logtoDict(self,domainList):
        end = len(domainList)
        for i in range(end,-1,-1):
            rejoined = self.rejoin(domainList[i : end])
            if rejoined != '':
                if rejoined in self.domains:
                    self.domains[rejoined] += 1
                else:
                    self.domains[rejoined] = 1


def makeOutputFile(fileName):
    '''
    Once all url's have been crawled. Use the global crawling dictionary and the url dictionary containing number of outlinks per url.
    Log all the information in a formatted manner to a file.
    '''
    current =  datetime.today() ## Get and log date and time of the web crawl 
    baseStr = "Making a crawler log on " + str(current.month) + " - " + str(current.day) + " - " + str(current.year) + " at Time " + str(current.hour) + " : " + str(current.minute) + " \n"
    baseStr += "Subdomain Logs\n" ##Display subdomain frequencies from the crawlerDict parameter
    for key in SUBDOMAINS:
        domainStr = "Domain/Subdomain: " + key
        frequency = "Frequency: " + str(SUBDOMAINS[key])
        formatString = "{0:<40} {1:>8}".format(domainStr,frequency)
        baseStr += (formatString + "\n")
    baseStr += ("Total Redirects:  " + str(GLOBAL_DICT["redirects"]) + "\n") ##Log redirect count
    baseStr += ("Invalid URLs:  " + str(GLOBAL_DICT["invalids"]) + " in total.\n") ##Log invalid url count
    baseStr += ("Non-absolute Urls Crawled:  " + str(GLOBAL_DICT["orig-relative"]) + "\n") ##Log total relative-urls encountered
    baseStr += ("Top url is:  " + COUNTER["url"]+ " at " + str(COUNTER["count"]) + " outlinks.\n") ## Log url with most outlinks
    log = open(fileName,"a") ##Open file for appending
    log.write(baseStr) ##Write all data
    log.close() ##Close file
