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
        self.loginURL = pllc.hostWebURL                             # pixiv login page
        # javascript console's headers dict
        self.loginHeader = pllc.SetUserAgentHeader()                # mate linux and windows
        # use post way to request service
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo))
        # get local cookie, create a opener for pixiv class
        self.cookie = cookielib.LWPCookieJar()                      # use last sheet to create a cookie-module
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
        # request to server, include url, headers, sheet, request way is post
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeader)
        # use new created opener(include cookies) to open, return server response sheet
        response = self.opener.open(request)
        # sometimes src has some error-code, use decode utf8 and encode gbk to resolve
        web_src = response.read().decode("UTF-8", "ignore").encode("GBK", "ignore")

        # http request situation code, ok is 200
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'website response successed'
        else:
            logContext = 'website response fatal, return code %d' % response.getcode()
        self.LogCrawlerWork(logPath, logContext)

        return web_src

    # save get images
    def SaveImageBinData(self, img_urls, base_pages, path, logPath):
        logContext = 'start to download target======>'
        self.LogCrawlerWork(logPath, logContext)

        for i, img_url in enumerate(img_urls):
            if os.name == 'posix':
                img_headers = {
                    'Accept': "image/webp,image/*,*/*;q=0.8",
                    'Accept-Encoding': "gzip, deflate, sdch",
                    'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
                    'Connection': "keep-alive",
                    # 'Host': img_url[8:9] + '.pixiv.net',          # host from last web page
                    # must add referer, or server will return a damn http error 403, 404
                    # copy from javascript console network request headers of image
                    'Referer': base_pages[i],  # request basic page
                    'User-Agent': pllc.useragentForLinuxBrowser,
                }
            elif os.name == 'nt':
                img_headers = {
                    'Accept': "image/webp,image/*,*/*;q=0.8",
                    'Accept-Encoding': "gzip, deflate, sdch",
                    'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
                    'Connection': "keep-alive",
                    # 'Host': img_url[8:9] + '.pixiv.net', # host from last web page
                    # must add referer, or server will return a damn http error 403, 404
                    # copy from javascript console network request headers of image
                    'Referer': base_pages[i],
                    'User-Agent': pllc.useragentForWindowsBrowser,
                }

            # use GET way to request server
            ## img_url_get_way = img_url + "?" + urllib.urlencode(pllc.get_way_info)
            img_request = urllib2.Request(url=img_url, headers=img_headers)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            urllib2.install_opener(opener)  # must install new created opener

            image_name = pllc.image_header + str(i)  # image name

            # pixiv website image format have jpg and png two format
            img_type_flag = 0  # replace png format, reset last
            try:
                img_response = urllib2.urlopen(img_request, timeout=30)
            except Exception, e:
                logContext = "check http error: " + str(e)
                self.LogCrawlerWork(logPath, logContext)
                img_type_flag += 1  # replace jpg format
                logContext = "this image maybe a manga comic or a jpg image"
                self.LogCrawlerWork(logPath, logContext)

                img_request = urllib2.Request(
                    url=img_url[0:-3] + 'jpg',  # img_http
                    ## data = json_login_data,                      # login cookie
                    headers=img_headers
                )
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                urllib2.install_opener(opener)  # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout=300)  # request timeout set longer

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    logContext = 'get target image ok'
                    self.LogCrawlerWork(logPath, logContext)
                    # image has two format: jpg
                    with open(path + '/' + image_name + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())  # do not decode
                    logContext = 'download no.%d finished' % i
                    self.LogCrawlerWork(logPath, logContext)

            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                logContext = 'get target image ok'
                self.LogCrawlerWork(logPath, logContext)

                # image has two format: png
                with open(path + '/' + image_name + '.png', 'wb') as png:
                    png.write(img_response.read())  # do not decode
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
