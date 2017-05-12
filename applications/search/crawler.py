#!/usr/bin/python
'''
Created on Oct 21, 2016

@author: Rohan Achar
'''
## Team information UC Irvine CS121: IR; Undergraduates; Spring 2017
## Joshua Pascascio, jpascasc@uci.edu, ID: 52192782
## Miguel Tolosa , tolosam@uci.edu, ID: 30392887
## Chang Shin Lee , changsl3@uci.edu, ID: 45754269
import logging
import logging.handlers
import os
import sys
import argparse
import uuid
import GlobalAnalytics

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from spacetime.client.frame import frame
#from applications.search.crawler_frame import CrawlerFrame, makeOutputFile
import applications.search.crawler_frame
logger = None
CrawlerFrame = applications.search.crawler_frame.CrawlerFrame

class Simulation(object):
    '''
    classdocs
    '''
    def __init__(self, address, port):
        '''
        Constructor
        '''
        frame_c = frame(address = "http://" + address + ":" + str(port) + "/", time_step = 1000)
        frame_c.attach_app(CrawlerFrame(frame_c))

        frame_c.run_async()
        frame.loop()

def SetupLoggers():
    global logger
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)
    #logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
    #flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
    #flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
    #logger.addHandler(flog)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CRAWLER'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)
if __name__== "__main__":
##    parser = argparse.ArgumentParser()
##    parser.add_argument('-a', '--address', type=str, help='Address of the distributing server')
##    parser.add_argument('-p', '--port', type=int, help='Port used by the distributing server')
##    args = parser.parse_args()
##    SetupLoggers()
##    sim = Simulation(args.address, args.port)
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--address', type=str, help='Address of the distributing server')
        parser.add_argument('-p', '--port', type=int, help='Port used by the distributing server')
        args = parser.parse_args()
        SetupLoggers()
        sim = Simulation(args.address, args.port)
    except:
        print("OS or Keyboard Interrupt")
    finally:
        print("DONE with Web Crawl")
        applications.search.crawler_frame.makeOutputFile("spacetime-crawler/logs/analytics.txt",applications.search.crawler_frame.analytics)
