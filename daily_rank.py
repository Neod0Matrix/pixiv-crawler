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

class DailyRankTop:
    """
        Pixiv website has a daily-rank top, ordinary and R18
        this class include fuction will gather all of that top
    """
    def __init__(self):
        """class include init process"""
        pp.__init__()
        # class inner global var
        self.workdir = pllc.privateFolder                           # setting global work directory
        self.logpath = pllc.logFilePath                             # setting global log path

    @staticmethod
    def GetEssentialInfo(self, wd, lp):
        """
            get input image count
            :param self:    self class
            :param wd:      work directory
            :param lp:      log save path
            :return:        crawl images count
        """
        # first create folder
        pp.MkDir(lp, wd)
        # select ordinary top or r18 top
        # transfer ascii string to number
        ormode = raw_input(pllc.SHELLHEAD + 'select ordinary top or r18 top(tap "o" or "r"): ')
        logContext = ''
        imgCnt = ''
        # setting max count, base on request web src
        ordinaryMaxcnt = 50
        r18MaxCnt = 100
        if ormode == 'o':
            # input a string for request image number
            imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter daily-rank top images count(max is %d): ' % ordinaryMaxcnt))
            while imgCnt > 50:
                print pllc.SHELLHEAD + 'input error, daily-rank top at most %d' % ordinaryMaxcnt
                imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter again(max is %d): ' % ordinaryMaxcnt))
            logContext = 'this python auto-crawler work to crawle pixiv website daily top %d images' % imgCnt
        elif ormode == 'r':
            # input a string for request image number
            imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter daily-rank R18 top images count(max is %d): ' % r18MaxCnt))
            while imgCnt > 100:
                print pllc.SHELLHEAD + 'input error, daily-rank R18 top at most %d' % r18MaxCnt
                imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter again(max is %d): ' % r18MaxCnt))
            logContext = 'this python auto-crawler work to crawle pixiv website daily top R18 %d images' % imgCnt
        pp.LogCrawlerWork(lp, logContext)
        # set to global var
        self.reqImageCnt = imgCnt
        self.drt_mode = ormode

        return imgCnt

    @staticmethod
    def GatherTargetList(self, ormode, img_nbr):
        """
            crawl dailyRank list
            :param self:    self class
            :param ormode:  oridinary mode or R18 mode
            :param img_nbr: images request count
            :return:        original images urls list
        """
        logContext = 'gather rank list======>'
        pp.LogCrawlerWork(self.logpath, logContext)

        request = ''
        if ormode == 'o':
            page_url = pllc.rankWebURL
            request = urllib2.Request(url=page_url,
                                      data=pllc.getData)
        elif ormode == 'r':
            page_url = pllc.rankWebURL_R18
            r18_headers = pllc.R18DailyRankRequestHeaders()
            request = urllib2.Request(url=page_url,
                                      data=pllc.getData,
                                      headers=r18_headers)
        else:
            print pllc.SHELLHEAD + "argv(s) error\n"
            exit()

        response = pp.opener.open(request, timeout=300)
        ## response = urllib2.urlopen(request, timeout=300)
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
            vaildWord = i[5:][:-1]  # pixiv may change its position sometimes
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

    def drtStartCrawler(self):
        """
            class main call process
            :return:    none
        """
        # prepare works
        nbr = self.GetEssentialInfo(self, self.workdir, self.logpath)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        pp.CamouflageLogin(self.logpath)
        # get ids and urls
        urls = self.GatherTargetList(self, self.drt_mode, nbr)
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
