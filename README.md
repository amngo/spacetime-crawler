# spacetime-crawler
The crawler apps using spacetime library 

## Installation 
* Use Python 2.7
* If you have pip installed already install. Then in this sequence 
  after issuing in terminal `git clone https://github.com/Mondego/spacetime-crawler`
* python -m pip install --user flask
* python -m pip install --user flask_restful
* python -m pip install --user requests
* python -m pip install --user pcc
* Then finally pip install spacetime
* When running the crawler make sure to be connected to the UCI VPN, you will get `ConnectionRefusedError` if you do not.

All these installation should allow all the files in <strong> spacetime crawler</strong> to run in the Python Shell without 
throwing any error

## Additional Libraries 
- In the crawler_frame.py, <strong>BeautifulSoup4, lxml, urllib2, urlparse, htmllib</strong> were used.
- To get BeautifulSoup, navigate to main Python directory on cmd type: `python -m pip install --user beautifulsoup4`
- To get lxml you can use a simple <a href="https://pypi.python.org/pypi/lxml/3.7.3" target="_blank" title="Click here to install to 
  your OS"> .exe installer</a>
- Other libraries are included with Python2.7 installation.
- Other helpful libraries might be <a href="https://cssselect.readthedocs.io/en/latest/" target="_blank" title="CSSSelector Documentation">CSSSelector</a> and html5lib(native to Python but can be slower in performance)
- Installation:
```
  python -m pip install --user cssselect
  python -m pip install --user html5lib
```

## Execute a sample crawl
  To run simulation of web crawling to up to 3000 urls in windows do, in Python folder:
  ```
  python spacetime-crawler/CopyCrawler.py -a amazon.ics.uci.edu -p 9050
  ```
  
## References
* <a href="https://docs.python.org/2/library/htmllib.html#htmllib.HTMLParser.anchor_bgn" target="_blank" title="HTML parsing library">htmllib</a>: HTML Document Parser
* <a href="https://docs.python.org/2/library/urlparse.html" target="_blank" title="Url parsing lib">urlparse</a>: Breaks down url 
  strings. Most helpful functions are likely `.urlparse , .urljoin , .urlsplit`
* <a href="http://lxml.de" target="_blank" title="lxml homepage">lxml library</a>. Needed for other HTMLParsing and is needed for 
  BeautifulSoup4 to run. Helpful libraries within lxml: `html , etree`
* <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank" title="BeautifulSoup4 Documentation">BeautifulSoup4</a>. To initialize the parser, properly use:
```python
  from bs4 import BeautifulSoup
  from urllib2 import urlopen
  urlString = "https://website.com/index.html"
  urlContent = urlopen(urlString) ##Attempts to make an HTTP Request and if successful, returns HTML file
  soupParser = BeautifulSoup(urlContent,"lxml")
  ## soupParser can now be used to parse the contents of the 'index.html' file now!
```
* To test, open, and request url's use <a href="https://docs.python.org/2/library/urllib2.html" target="_blank" title="Python's main url 
  function library">urllib2</a>. Most useful methods for this kind of program are `.urlopen , .Request`
  
### Using The Test File mainCrawler.py
1. Make sure you have the full repository cloned using git onto to your local system. I would recommend you place in the Python 
  directory where all the standard libaries are stored for me it is in:
  * `C:\Python27\`
  * Although for others it might be, on Windows:
    ```
    C:\Users\Username\AppData\Local\Programs\Python27\
    ```
2. Put in the root of the spacetime-crawler directory on your system, it might complicate the way that import statements are handled if 
   it is stored somewhere else, so try something like:
  * `C:\Users\Username\AppData\Local\Programs\Python27\spacetime-crawler
3. Once that is done run the file either in IDLE by 
  1. Opening the file -> Right Click -> Edit With IDLE
  2. Click Run -> Run Module or Key: F5
  3. Once there a `(cmd)` prompt will open asking for commands
  4. To run the crawler just type `download` followed by a url you will like to check out and crawl (Note only .ics.uci.edu) domains 
     will retrieve valid results.. Others result in timeout or connection errors but will not halt the program)
4. For remotely just double click or execute the on the command-line with no arguments and it will automatically crawl the subdomain,   
   ics.uci.edu. This will run infinitely but can be stopped with Ctrl^Z 
5. The crawler will display what url's it has downloaded and what it failed to by displaying a timeout message in red. (Successful 
    downloads are usually in blue)
6. All successful url downloads or checks are written to a file called `successfulurls.txt` once finished. All are valid URL's some are 
   relative to certain paths though so in other parts of the program they may need to be joined with `urljoin` method.

## Functions Added
* Located in spacetime-crawler/applications/search/crawler_frame.py, near bottom
* Added/Modified Functions are: get_url_content, extract_next_links, is_valid. The file should have their documentation
