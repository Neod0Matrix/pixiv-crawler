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
        self.workdir = pllc.privateFolder
        self.logpath = pllc.logFilePath

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

        infoPattern = re.compile(pllc.rankTitleRegex, re.S)         # use regex, find dailyRank art works messages
        dataCapture = re.findall(infoPattern, web_src)              # findall return a tuple include 5 members

        # build original image url
        vwPattern = re.compile(pllc.rankVWRegex, re.S)              # gather vaild word
        vwCapture = re.findall(vwPattern, web_src)
        targetURL =[]
        for i in vwCapture:
            i = 'https://i.pximg.net/img-original/img/' + i[6:][:-1] + '_p0.png' # default set to png
            logContext = i
            priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
            targetURL.append(i)
        logContext = 'daily-rank original images target gather successed'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
        # gather all of info
        for i in dataCapture:
            print i[0], i[1], i[2], i[3], i[4]                      # list all members
        logContext =  'daily-rank page request successed, get the info of pictures and authors'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        # save info as another file
        infos = 'top ' + str(img_nbr) + ' messages:\n'
        # findall class max get 50 memebr from list
        for i in dataCapture[:img_nbr]:
            # rewrite info content to file
            infos += '------------no.%s-----------\n' % i[0]        # artwork title
            infos += 'name: %s\nilluster: %s\nid: %s\n' % (i[1], i[2], i[4])
        with open(pllc.illustInfoFilePath, 'w+') as text:
            text.write(infos.encode('UTF-8'))

        aw_ids = [i[4] for i in dataCapture]
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
