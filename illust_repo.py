#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get a illust all repo images

import urllib2, cookielib, re, json, urllib                         # crawler depends
import datetime, os, string
import pllc, priv_lib                                               # local lib

# create a class for pixiv dailyRank top
class IllustRepoAll:
    # class include init process
    def __init__(self):
        priv_lib.PrivateLib().__init__()
        # global illust id
        self.illustInputID = raw_input(pllc.SHELLHEAD + 'enter you want to crawl illuster id: ')

    @staticmethod
    def GetInputEssentialInfo(self):
        illustHomeFolder = pllc.SetOSHomeFolder() + self.illustInputID + '/'
        illustLogFilePath = illustHomeFolder + 'PixivCrawlerLog.log'
        # create illust homefolder
        priv_lib.PrivateLib().MkDir(illustLogFilePath, illustHomeFolder)

        return illustLogFilePath

    # craw illust artwork count
    @staticmethod
    def CheckCrawlTargetCnt(self, logPath):
        cnt_url = pllc.illustHomeURL + self.illustInputID           # get illust artwork count mainpage url
        # build http request
        request = urllib2.Request(cnt_url)
        response = priv_lib.PrivateLib().opener.open(request)
        web_src = response.read().decode('UTF-8')                   # read it, and decode with UTF-8

        pattern = re.compile(pllc.illustAWCntRegex(self.illustInputID), re.S)  # use regex, find dailyRank art works messages
        dataCapture = re.findall(pattern, web_src)                  # findall return a tuple include 5 members

        maxCnt = string.atoi(dataCapture[0][-4:-1])                 # get illust max artwork count
        # input want image count
        capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                        + 'enter you want to crawl image count(must <= %d): ' % maxCnt))
        # count error
        while (capCnt > maxCnt) or (capCnt <= 0):
            capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                        + 'error, input count must <= %d and not 0: ' % maxCnt))
        logContext = "check collect illustID:" + self.illustInputID + " images:%d" % capCnt
        priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)

        return capCnt

    # craw illust artwork count
    @staticmethod
    def CrawlAllTargetURL(self, logPath):
        urlTarget = pllc.illustArtworkIndex(self.illustInputID)     # get mainpage all 20 images url

        # build a mainpage request
        mainPageHeader = pllc.SetUserAgentForMainPage(urlTarget)
        request = urllib2.Request(url=urlTarget, headers=mainPageHeader)

        # build and install opener
        cookieHandler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
        opener = urllib2.build_opener(cookieHandler)
        urllib2.install_opener(opener)

        # open webpage, get web src, try two way
        # response = opener.open(request)
        response = urllib2.urlopen(request, timeout=300)
        # web_src = response.read().decode("UTF-8", "ignore").encode("GBK", "ignore")
        web_src = response.read().decode("UTF-8")
        if response.getcode() == pllc.reqSuccessCode:
            logContext = "mainpage response successed"
            priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)

        pattern = re.compile(pllc.imgThumbnailRegex, re.S)          # use regex, find dailyRank art works messages
        urlCapture = re.findall(pattern, web_src)[1:20]             # findall return a tuple include 5 members

        vaildWords = []
        for i in urlCapture:
            vaildWords.append(i[-47:-19])                           # get valid word from thumbnail url

        return vaildWords


    def iraStartCrawler(self):
        # collect essential info
        logFilePath = self.GetInputEssentialInfo(self)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        priv_lib.PrivateLib().CrawlerSignIn(logFilePath)
        # get capture image count
        crawCnt = self.CheckCrawlTargetCnt(self, logFilePath)
        self.CrawlAllTargetURL(self, logFilePath)

        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        priv_lib.PrivateLib().LogCrawlerWork(logFilePath, logContext)
        # finish
        priv_lib.PrivateLib().crawlerFinishWork(logFilePath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
