#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to get pixiv dailyRank top images

import urllib2, re                                                  # crawler depends
import datetime, string
import pllc, priv_lib                                               # local lib

pp = priv_lib.PrivateLib()
pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class DailyRankTop:
    # class include init process
    def __init__(self):
        pp.__init__()
        # class inner global var
        self.workdir = pllc.privateFolder                           # setting global work directory
        self.logpath = pllc.logFilePath                             # setting global log path

    # get input image count
    @staticmethod
    def GetEssentialInfo(self, wd, lp):
        # first create folder
        pp.MkDir(lp, wd)
        # input a string for request image number, transfer string to number
        imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter daily-rank top images count(max is 50): '))
        logContext = 'this python auto-crawler work to crawle pixiv website daily top %d images' % imgCnt
        pp.LogCrawlerWork(lp, logContext)
        self.reqImageCnt = imgCnt

        return imgCnt

    # crawl dailyRank list
    @staticmethod
    def GatherTargetList(self, img_nbr):
        logContext = 'gather rank list======>'
        pp.LogCrawlerWork(self.logpath, logContext)

        page_url = pllc.rankWebURL
        request = urllib2.Request(url=page_url,
                                  data=pp.getData)
        response = pp.opener.open(request, timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'website response successed'
        else:
            # response failed, you need to check network status
            logContext = 'website response fatal, return code %d' % response.getcode()
        pp.LogCrawlerWork(self.logpath, logContext)
        web_src = response.read().decode("UTF-8", "ignore")

        # build original image url
        vwPattern = re.compile(pllc.rankVWRegex, re.S)
        vwCapture = re.findall(vwPattern, web_src)
        targetURL = []
        for i in vwCapture[:img_nbr]:
            vaildWord = i[5:][:-1]                                  # pixiv may change its position sometimes
            targetURL.append(pllc.imgOriginalheader + vaildWord + pllc.imgOriginaltail)

        # gather info of artworks
        infoPattern = re.compile(pllc.rankTitleRegex, re.S)
        dataCapture = re.findall(infoPattern, web_src)
        logContext = 'top ' + str(img_nbr) + ' info======>'
        pp.LogCrawlerWork(self.logpath, logContext)
        aw_ids = []                                                 # artwork id
        self.basePages = []                                         # request original image need referer
        for k, i in enumerate(dataCapture[:img_nbr]):
            logContext = '------------no.%s-----------' % i[0]      # artwork array
            pp.LogCrawlerWork(self.logpath, logContext)
            logContext = 'name: %s illustrator: %s id: %s url: %s' % (i[1], i[2], i[4], targetURL[k])
            pp.LogCrawlerWork(self.logpath, logContext)
            aw_ids.append(i[4])
            self.basePages.append(pllc.baseWebURL + i[4])           # every picture url address: base_url address + picture_id

        return targetURL

    # class main call process
    def drtStartCrawler(self):
        # prepare works
        nbr = self.GetEssentialInfo(self, self.workdir, self.logpath)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        pp.CrawlerSignIn(self.logpath)
        # get ids and urls
        urls = self.GatherTargetList(self, nbr)
        # save images
        pp.SaveImageBinData(urls, self.basePages, self.workdir, self.logpath)
        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        pp.LogCrawlerWork(self.logpath, logContext)
        # finish
        pp.crawlerFinishWork(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
