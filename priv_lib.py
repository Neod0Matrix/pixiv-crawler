#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to create a private library use in this crawler

import urllib, urllib2, cookielib, os, json                         # crawler depends
import pllc                                                         # messages

# create a class for pixiv dailyRank top
class PrivateLib:
    # class include init process
    def __init__(self):
        # request sheet
        self.loginURL = pllc.hostWebURL                             # pixiv login page
        # javascript console's headers dict
        # only use in linux's google chrome
        self.loginHeader = pllc.loginDataHeader
        # use post way to request service
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo))
        # get local cookie, create a opener for pixiv class
        self.cookie = cookielib.LWPCookieJar()                      # use last sheet to create a cookie-module
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler)

    # work log save
    def LogCrawlerWork (self, logPath, logInfo):
        # this log file must be a new file
        logFile = open(logPath, 'a+')                               # add context to file option 'a+'
        print pllc.SHELLHEAD + logInfo                              # with shell header
        print >> logFile, pllc.SHELLHEAD + logInfo

    # create a file directory to save pictures
    def MkDir(self, logPath, folder):
        # create a folder to save picture
        isFolderExisted = os.path.exists(folder)
        if not isFolderExisted:
            os.makedirs(folder)
            logContext = 'folder create successed'
        else:
            logContext = 'the folder has already existed'
        # remove old log file
        if os.path.exists(logPath):
            os.remove(logPath)
        self.LogCrawlerWork(logPath, logContext)

        return folder

    # first try to request website link
    def CrawlerSignIn(self, logPath):
        # request to server, include url, headers, sheet, request way is post
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeader)
        # use new created opener(include cookies) to open, return server response sheet
        response = self.opener.open(request)
        content = response.read().decode('utf-8')                   # read it, and decode with UTF-8

        # http request situation code, ok is 200
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'website response successed'
        else:
            logContext = 'website response fatal, return code %d' % response.getcode()
        self.LogCrawlerWork(logPath, logContext)

        return response.getcode()                                   # run status flag

    # work over
    def crawlerFinishWork (self, logPath):
        # logging info
        logContext = "crawler work finished, log time: " + pllc.excFinishTime
        self.LogCrawlerWork(logPath, logContext)
        logContext = "\n"  # print a empty row
        self.LogCrawlerWork(logPath, logContext)
        logContext = \
            'copyright @' + pllc.__laboratory__ + ' technology support\n' \
                                                  'code by ' + pllc.__organization__ + '@' + pllc.__author__ + '\n' \
            + pllc.__version__  # print version string
        self.LogCrawlerWork(logPath, logContext)

        # open filebox to watch result
        if pllc.os_name == 'posix':
            os.system(pllc.fileManager + ' ' + pllc.SetOSHomeFolder())
            exit()  # after open folder exit process

# =====================================================================
# code by </MATRIX>@Neod Anderjon
