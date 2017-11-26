#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to get pixiv rank top images

import urllib2, re                                                  # crawler depends
import datetime, string
import pllc, priv_lib                                               # local lib

pp = priv_lib.PrivateLib()
pllc.EncodeDecodeResolve()

class DailyRankTop:
    """
        Pixiv website has a rank top, ordinary and R18, daily, weekly, monthly
        this class include fuction will gather all of those ranks
    """
    def __init__(self):
        """class include init process"""
        # class inner global var
        self.workdir = pllc.privateFolder                           # setting global work directory
        self.logpath = pllc.logFilePath                             # setting global log path
        self.htmlpath = pllc.htmlFilePath                           # setting global html path

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
        ormode = raw_input(pllc.SHELLHEAD + 'select ordinary top or r18 top(tap "o"&"1" or "r"&"2"): ')
        imgCnt = ''
        # setting max count, base on request web src
        ordinaryMaxcnt = 50
        r18MaxCnt = 50
        if ormode == 'o' or ormode == '1':
            # input a string for request image number
            imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter crawl rank top image count(max is %d): ' % ordinaryMaxcnt))
            while imgCnt > ordinaryMaxcnt:
                print pllc.SHELLHEAD + 'input error, rank top at most %d' % ordinaryMaxcnt
                imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter again(max is %d): ' % ordinaryMaxcnt))
        elif ormode == 'r' or ormode == '2':
            # input a string for request image number
            imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter crawl rank R18 top image count(max is %d): ' % r18MaxCnt))
            while imgCnt > r18MaxCnt:
                print pllc.SHELLHEAD + 'input error, rank R18 top at most %d' % r18MaxCnt
                imgCnt = string.atoi(raw_input(pllc.SHELLHEAD + 'enter again(max is %d): ' % r18MaxCnt))
        else:
            print pllc.SHELLHEAD + "argv(s) error\n"
            ormode = None
        # set to global var
        self.reqImageCnt = imgCnt
        self.rtn_mode = ormode

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
        rankWord = ''
        page_url = ''
        request = ''
        if ormode == 'o' or ormode == '1':
            dwm = raw_input(pllc.SHELLHEAD + 'select daily(1)/weekly(2)/monthly(3) rank top: ')
            if dwm == '1':
                page_url = pllc.dailyRankURL
                rankWord = 'daily'
            elif dwm == '2':
                page_url = pllc.weeklyRankURL
                rankWord = 'weekly'
            elif dwm == '3':
                page_url = pllc.monthlyRankURL
                rankWord = 'monthly'
            else:
                print pllc.SHELLHEAD + "argv(s) error\n"
            request = urllib2.Request(url=page_url, data=pllc.getData)
            logContext = 'crawler set target to %s rank top %d image(s)' % (rankWord, img_nbr)
            pp.LogCrawlerWork(self.logpath, logContext)
        elif ormode == 'r' or ormode == '2':
            dwm = raw_input(pllc.SHELLHEAD + 'select daily(1)/weekly(2) R18 rank top: ')
            if dwm == '1':
                page_url = pllc.dailyRankURL_R18
                rankWord = 'daily'
            elif dwm == '2':
                page_url = pllc.weeklyRankURL_R18
                rankWord = 'weekly'
            else:
                print pllc.SHELLHEAD + "argv(s) error\n"
            r18_headers = pllc.R18DailyRankRequestHeaders()
            request = urllib2.Request(url=page_url, data=pllc.getData, headers=r18_headers)
            logContext = 'crawler set target to %s r18 rank top %d image(s)' % (rankWord, img_nbr)
            pp.LogCrawlerWork(self.logpath, logContext)
        else:
            print pllc.SHELLHEAD + "argv(s) error\n"
        ## request.add_data(pllc.getData)
        ## pp.opener.addheaders = pllc.R18DailyRankRequestHeaders()
        ## urllib2.install_opener(pp.opener)
        response = pp.opener.open(request, timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'website response successed'
        else:
            # response failed, you need to check network status
            logContext = 'website response fatal, return code %d' % response.getcode()
        pp.LogCrawlerWork(self.logpath, logContext)
        web_src = response.read().decode("UTF-8", "ignore")
        ## pp.testSavehtml(self.workdir, web_src, self.logpath)

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

    def rtnStartCrawler(self):
        """
            class main call process
            :return:    none
        """
        # prepare works
        nbr = self.GetEssentialInfo(self, self.workdir, self.logpath)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        pp.ProxyServerCrawl(self.logpath)
        pp.CamouflageLogin(self.logpath)
        # get ids and urls
        urls = self.GatherTargetList(self, self.rtn_mode, nbr)
        # save images
        pp.TargetImageDownload(urls, self.basePages, self.workdir, self.logpath)
        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        pp.LogCrawlerWork(self.logpath, logContext)
        # finish
        pp.htmlBuilder(self, self.workdir, self.htmlpath, self.logpath)
        pp.crawlerFinishWork(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
