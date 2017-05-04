from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
from urlparse import urlparse,urljoin


def countDomains(domain):
    count = 0
    for i in domain:
        if i == ".":
            count += 1
    return count
def rejoin(domainList):
    baseStr = ""
    for i in domainList:
        baseStr += i + "."
    baseStr = "." + baseStr
    return baseStr[0:len(baseStr) - 1]

def splitDomains(url):
    baseUrl = url.split("/")[2].strip("www.")
    subdomains = baseUrl.split(".")
    indexList = []
    logtoDict(subdomains,global_dict)
    return baseUrl

def logtoDict(domainList,referenceDict):
    end = len(domainList)
    for i in range(end,-1,-1):
        rejoined = rejoin(domainList[i : end])
        if rejoined != '':
            if rejoined in referenceDict:
                referenceDict[rejoined] += 1
            else:
                referenceDict[rejoined] = 1
def prettyFormat(keyList):
    for i in keyList:
        print("Domain: " + i[0] + " Frequency: " + str(i[1]))
if __name__ == "__main__":
    print("LOGGING FILE")
    example_list = ['http://www.ics.uci.edu/~eppstein/pubs/p-qpack.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://www.ics.uci.edu/~xge/', 'http://www.ics.uci.edu/~smyth/',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/The-distribution-of-cycle-lengths-in-graphical-models-for-iterative-decoding.html',
                'http://www.ics.uci.edu/~eppstein/pubs/geom-circle.html', 'http://www.ics.uci.edu/~eppstein/junkyard/tangencies/apollonian.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html', 'http://fano.ics.uci.edu/cites/Document/Tangent-spheres-and-triangle-centers.html',
                'http://www.ics.uci.edu/~josephw/', 'http://www.ics.uci.edu/~eppstein/pubs/graph-path.html', 'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Fast-approximation-of-centrality.html', 'http://www.ics.uci.edu/~eppstein/pubs/p-3color.html',
                'http://www.ics.uci.edu/~eppstein/pubs/p-3color2.html', 'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://www.ics.uci.edu/~eppstein/pubs/geom-deep.html', 'http://www.ics.uci.edu/~eppstein/pubs/p-multivariate.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html', 'http://fano.ics.uci.edu/cites/Document/Computing-the-depth-of-a-flat.html', 
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Internet-packet-filter-management-and-rectangle-geometry.html',
                'http://www.ics.uci.edu/~eppstein/pubs/graph-color.html', 'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Small-maximal-independent-sets-and-faster-exact-graph-coloring.html',
                'http://www.ics.uci.edu/~eppstein/pubs/geom-lp.html', 'http://www.ics.uci.edu/~eppstein/pubs/geom-circle.html',
                'http://www.ics.uci.edu/~eppstein/pubs/gdraw.html', 'http://www.ics.uci.edu/~eppstein/pubs/geom-hyperbolic.html',
                'http://www.ics.uci.edu/~eppstein/pubs/geom-tri.html', u'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Optimal-Moebius-transformations-for-information-visualization-and-meshing.html',
                'http://www.ics.uci.edu/~eppstein/pubs/geom-lp.html', 'http://www.ics.uci.edu/~eppstein/pubs/geom-zono.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html', 
                'http://fano.ics.uci.edu/cites/Document/Optimization-over-zonotopes-and-training-support-vector-machines.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html', 'http://fano.ics.uci.edu/cites/Document/Hinged-kite-mirror-dissection.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html', 'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Flipping-cubical-meshes.html', 'http://www.ics.uci.edu/~eppstein/pubs/p-thickness.html',
                'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Separating-geometric-thickness-from-book-thickness.html',
                'http://www.ics.uci.edu/~lueker/', 'http://www.ics.uci.edu/~eppstein/bibs/eppstein.html',
                'http://fano.ics.uci.edu/cites/Document/Global-optimization-of-mesh-quality.html',
                'http://www.ics.uci.edu/~eppstein/pubs/year.html', 'http://www.ics.uci.edu/~eppstein/pubs/',
                'http://www.ics.uci.edu/~eppstein/', 'http://www.ics.uci.edu/~theory/',
                'http://www.ics.uci.edu/~eppstein/pubs/filter.html']
    global_dict = {}
    for i in example_list:
        splitDomains(i)
    formatted = sorted(global_dict.items(), key = lambda item: (countDomains(item[0]),item[1]))
    prettyFormat(formatted)


