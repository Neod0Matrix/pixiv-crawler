#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get pixiv dailyRank top images

import urllib2, re                                                  # crawler depends
import datetime, string
import pllc, priv_lib                                               # local lib

pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class DailyRankTop:
    # class include init process
    def __init__(self):
        priv_lib.PrivateLib().__init__()
        # class inner global var
        self.workdir = pllc.privateFolder                           # setting global work directory
        self.logpath = pllc.logFilePath                             # setting global log path

    # get input image count
    @staticmethod
    def GetEssentialInfo(self, wd, lp):
        # first create folder
        priv_lib.PrivateLib().MkDir(lp, wd)
        # input a string for request image number, transfer string to number
        imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter daily-rank top images count(max is 50): '))
        logContext = 'this python auto-crawler work to crawle pixiv website daily top %d images' % imgCnt
        priv_lib.PrivateLib().LogCrawlerWork(lp, logContext)

        return imgCnt

    # crawl dailyRank list
    @staticmethod
    def GatherTargetList(self, img_nbr):
        logContext = 'crawl rank list======>'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        rank_url = pllc.rankWebURL
        request = urllib2.Request(rank_url)
        response = priv_lib.PrivateLib().opener.open(request)
        web_src = response.read().decode("UTF-8", "ignore")

        # gather info of artworks
        infoPattern = re.compile(pllc.rankTitleRegex, re.S)
        dataCapture = re.findall(infoPattern, web_src)

        # build original image url
        vwPattern = re.compile(pllc.rankVWRegex, re.S)
        vwCapture = re.findall(vwPattern, web_src)
        targetURL = []
        # only log need count of image
        for i in vwCapture[:img_nbr]:
            i = pllc.imgOriginalheader + i[5:][:-1] + pllc.imgOriginaltail
            logContext = i
            priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
            targetURL.append(i)
        logContext = 'daily-rank original images target gather successed'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        logContext = 'top ' + str(img_nbr) + ' info======>'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
        for i in dataCapture[:img_nbr]:
            logContext = '------------no.%s-----------' % i[0]      # artwork array
            priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
            logContext = 'name: %s illuster: %s id: %s' % (i[1], i[2], i[4])
            priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        aw_ids = [i[4] for i in dataCapture[:img_nbr]]
        self.basePages = [pllc.baseWebURL + str(i) for i in aw_ids] # every picture url address: base_url address + picture_id

        return targetURL[:img_nbr]                                  # only return need image number

    # class main call process
    def drtStartCrawler(self):
        # prepare works
        nbr = self.GetEssentialInfo(self, self.workdir, self.logpath)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        priv_lib.PrivateLib().CrawlerSignIn(self.logpath)
        # get ids and urls
        urls = self.GatherTargetList(self, nbr)
        # save images
        priv_lib.PrivateLib().SaveImageBinData(urls, self.basePages, self.workdir, self.logpath)
        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
        # finish
        priv_lib.PrivateLib().crawlerFinishWork(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
