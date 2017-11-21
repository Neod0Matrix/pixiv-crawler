#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to create a private library use in this crawler

import urllib, urllib2, cookielib, os, json                         # crawler depends
import sys
import pllc                                                         # messages

pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class PrivateLib:
    # class include init process
    def __init__(self):
        # request sheet
        self.loginURL = pllc.hostWebURL                             # pixiv website home page
        # javascript console's headers dict
        self.loginHeader = pllc.SetUserAgentHeader()                # build request headers
        # use post way to request service
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo))
        # get local cookie, create a opener for pixiv class
        self.cookie = cookielib.LWPCookieJar()                      # build cookie module
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler)

    # work log save
    def LogCrawlerWork(self, logPath, logInfo):
        # this log file must be a new file
        logFile = open(logPath, 'a+')                               # add context to file option 'a+'
        print pllc.SHELLHEAD + logInfo                              # with shell header
        print >> logFile, pllc.SHELLHEAD + logInfo                  # write to log

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
        # test self.opener work
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeader)
        response = self.opener.open(request)
        # try to test website response
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'website response successed'
        else:
            # response failed, you need to check network status
            logContext = 'website response fatal, return code %d' % response.getcode()
        self.LogCrawlerWork(logPath, logContext)

    # save get images
    def SaveImageBinData(self, img_urls, base_pages, imgPath, logPath):
        logContext = 'start to download target======>'
        self.LogCrawlerWork(logPath, logContext)

        for i, img_url in enumerate(img_urls):
            img_headers = pllc.SetImageRequestHeader(base_pages[i]) # reset headers with basic pages
            # use GET way to request server
            ## img_url_get_way = img_url + "?" + urllib.urlencode(pllc.get_way_info)
            img_request = urllib2.Request(url=img_url, headers=img_headers)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            urllib2.install_opener(opener)                          # must install new created opener

            # pixiv website image format have jpg and png two format
            img_type_flag = 0                                       # replace png format, reset last
            img_id = img_url[57:][:-7]                              # cut id from url
            image_name = str(i) + '-' + img_id                      # image name
            try:
                img_response = urllib2.urlopen(img_request, timeout=60)
            except Exception, e:
                ## logContext = "check http error: " + str(e)
                ## self.LogCrawlerWork(logPath, logContext)
                img_type_flag += 1  # replace jpg format
                ## logContext = "this image may be a manga comic or a jpg image"
                ## self.LogCrawlerWork(logPath, logContext)

                img_request = urllib2.Request(
                    url=img_url[0:-3] + 'jpg',                      # change to jpg format tail
                    headers=img_headers
                )
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                urllib2.install_opener(opener)                      # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout=300) # request timeout set longer

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    logContext = 'capture target jpg image ok'
                    self.LogCrawlerWork(logPath, logContext)
                    # image has two format: jpg
                    # image is bin data, don't decode it, just read() ok
                    with open(imgPath + '/' + image_name + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())
                    logContext = 'download no.%d image finished' % i
                    self.LogCrawlerWork(logPath, logContext)

            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                logContext = 'capture target png image ok'
                self.LogCrawlerWork(logPath, logContext)

                # image has two format: png
                with open(imgPath + '/' + image_name + '.png', 'wb') as png:
                    png.write(img_response.read())
                logContext = 'download no.%d finished' % i
                self.LogCrawlerWork(logPath, logContext)

    # work over
    def crawlerFinishWork(self, logPath):
        # logging info
        logContext = "crawler work finished, log time: " + pllc.excFinishTime
        self.LogCrawlerWork(logPath, logContext)
        logContext = \
            'copyright @' + pllc.__laboratory__ + ' ' + pllc.__organization__\
            + ' technology support\n' \
            'code by ' + pllc.__organization__ + '@' + pllc.__author__ + '\n' \
            + 'version: ' + pllc.__version__
        self.LogCrawlerWork(logPath, logContext)

        # open filebox to watch result
        if os.name == 'posix':
            os.system(pllc.fileManager + ' ' + pllc.SetOSHomeFolder())
            sys.exit(1)                                             # after open folder exit process

# =====================================================================
# code by </MATRIX>@Neod Anderjon
