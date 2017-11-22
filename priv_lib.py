#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to create a private library use in this crawler

import urllib, urllib2, cookielib, os, json                         # crawler depends
import pllc                                                         # messages

pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class PrivateLib:
    # class include init process
    def __init__(self):
        self.loginURL = pllc.hostWebURL                             # pixiv website home page
        self.loginHeader = pllc.InitLoginHeaders()                  # build request headers
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo)) # add post way
        self.cookie = cookielib.LWPCookieJar()                      # build cookie module
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler)      # build opener pack
        urllib2.install_opener(self.opener)                         # install this pack

    # work log save
    @staticmethod
    def LogCrawlerWork(logPath, logInfo):
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
            img_headers = pllc.OriginalImageRequestHeaders(base_pages[i]) # reset headers with basic pages
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
            # http error because only use png format to build url
            # after except error, url will be changed to jpg format
            except Exception, e:
                ## logContext = "check http error: " + str(e)
                ## self.LogCrawlerWork(logPath, logContext)
                ## logContext = "this image may be a manga comic or a jpg image"
                ## self.LogCrawlerWork(logPath, logContext)
                img_type_flag += 1
                chajpgurl = img_url[0:-3] + 'jpg'                   # replace to jpg format
                img_request = urllib2.Request(
                    url=chajpgurl,
                    headers=img_headers
                )
                # rebuild opener
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                urllib2.install_opener(opener)                      # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout=300) # request timeout set longer

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    logContext = 'capture target jpg image ok'
                    self.LogCrawlerWork(logPath, logContext)
                    with open(imgPath + '/' + image_name + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())
                    logContext = 'download no.%d image finished' % i
                    self.LogCrawlerWork(logPath, logContext)

            # no http error, image is png format, continue request
            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                logContext = 'capture target png image ok'
                self.LogCrawlerWork(logPath, logContext)
                with open(imgPath + '/' + image_name + '.png', 'wb') as png:
                    png.write(img_response.read())
                logContext = 'download no.%d image finished' % i
                self.LogCrawlerWork(logPath, logContext)

    # work over
    def crawlerFinishWork(self, logPath):
        # logging info
        logContext = "crawler work finished, log time: " + pllc.ymdhms
        self.LogCrawlerWork(logPath, logContext)
        logContext = \
            'copyright @' + pllc.__laboratory__ + ' ' + pllc.__organization__   \
            + ' technology support\n'                                           \
            'code by ' + pllc.__organization__ + '@' + pllc.__author__ + '\n'   \
            + 'version: ' + pllc.__version__
        self.LogCrawlerWork(logPath, logContext)
        # open file-manager to check result
        os.system(pllc.OSFileManager() + ' ' + pllc.workDir)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
