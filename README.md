# spacetime-crawler
The crawler apps using spacetime library 

## Installation 
* Use Python 2.7
* If you have pip installed already install in this sequence 
  after issuing in terminal `git clone https://github.com/Mondego/spacetime-crawler`
* python -m pip install --user flask
* python -m pip install --user flask_restful
* python -m pip install --user requests
* python -m pip install --user pcc
* Then finally pip install spacetime
* When running the crawler make sure to be installed to the UCI VPN, you will get `ConnectionRefusedError` if you do not.

All these installation should allow all the files in <strong> spacetime crawler</strong> to run in the Python Shell without 
throwing any error

### Using The Test File mainCrawler.py
1. Make sure you have the full repository cloned using git onto to your local system. I would recommend you place in the Python directory where all the standard libaries are stored for me it is in:
  * `C:\Python27\`
  * Although for others it might be, on Windows:
    `C:\Users\Username\AppData\Local\Programs\Python27\`
2. Put in the root of the spacetime-crawler directory on your system, it might complicate the way that import statements are handled if it is stored somewhere else, so try something like:
  * `C:\Users\Username\AppData\Local\Programs\Python27\spacetime-crawler
3. Once that is done run the file either in IDLE by 
  1. Opening the file -> Right Click -> Edit With IDLE
  2. Click Run -> Run Module or Key: F5
  3. Once there a `(cmd)` prompt will open asking for commands
  4. To run the crawler just type `download` followed by a url you will like to check out and crawl (Note only .ics.uci.edu) domains will 
     retrieve valid results.. Others result in timeout or connection errors but will not halt the program)
4. For remotely just double click or execute the on the command-line with no arguments and it will automatically crawl the subdomain,   
   ics.uci.edu. This will run infinitely but can be stopped with Ctrl^Z 
5. The crawler will display what url's it has downloaded and what it failed to by displaying a timeout message in red. (Successful 
    downloads are usually in blue)
6. All successful url downloads or checks are written to a file called `successfulurls.txt` once finished. All are valid URL's some are relative to certain paths though so in other parts of the program they may need to be joined with `urljoin` method.

## Functions Added
* Located in spacetime-crawler/applications/search/crawler_frame.py, near bottom
* Added/Modified Functions are: get_url_content, extract_next_links, is_valid. The file should have their documentation
