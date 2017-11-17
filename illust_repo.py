#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get a illust all repo images

import urllib2, cookielib, re, os, json, string                     # crawler depends
import pllc, priv_lib

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
    def CrawlTargetMaxCnt(self):
        cnt_url = pllc.illustHomeURL + self.illustInputID
        # build http request
        request = urllib2.Request(cnt_url)
        response = priv_lib.PrivateLib().opener.open(request)
        web_src = response.read().decode('UTF-8')                   # read it, and decode with UTF-8

        pattern = re.compile(pllc.illustAWCntRegex(self.illustInputID), re.S)  # use regex, find dailyRank art works messages
        dataCapture = re.findall(pattern, web_src)                  # findall return a tuple include 5 members
        maxCnt = string.atoi(dataCapture[0][-4:-1])                 # get illust max artwork count

        return maxCnt

    # input want image count
    @staticmethod
    def GetInputCrawlCnt(self, max_cnt):
        capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                                       + 'enter you want to crawl image count(must <= %d): ' % max_cnt))
        # count error
        while (capCnt > max_cnt) or (capCnt <= 0):
            capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                                        + 'error, rewrite you want to crawl image count(must <= %d, not 0): ' % max_cnt))

        return capCnt

    def iraStartCrawler(self):
        # collect essential info
        logFilePath = self.GetInputEssentialInfo(self)
        # sign in to pixiv
        priv_lib.PrivateLib().CrawlerSignIn(logFilePath)
        # get capture image count
        crawCnt = self.CrawlTargetMaxCnt(self)
        actCnt = self.GetInputCrawlCnt(self, crawCnt)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
