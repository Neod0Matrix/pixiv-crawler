#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get a illust all repo images

import urllib2, cookielib, re                                       # crawler depends
import datetime, string
import pllc, priv_lib                                               # local lib

pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class IllustRepoAll:
    # class include init process
    def __init__(self):
        priv_lib.PrivateLib().__init__()
        # global illust id
        self.illustInputID \
            = raw_input(pllc.SHELLHEAD + 'enter you want to crawl illuster id: ')

    @staticmethod
    def GetInputEssentialInfo(self):
        illustHomeFolder = pllc.SetOSHomeFolder() + self.illustInputID
        self.workdir = illustHomeFolder                             # setting global work directory
        illustLogFilePath = illustHomeFolder + pllc.logFileName
        # create illust homefolder
        priv_lib.PrivateLib().MkDir(illustLogFilePath, illustHomeFolder)

        return illustLogFilePath

    # craw illust artwork count
    @staticmethod
    def GatherIndexInfo(self, logPath):
        cnt_url = pllc.illustHomeURL + self.illustInputID           # get illust artwork count mainpage url
        # build http request
        request = urllib2.Request(cnt_url)
        response = priv_lib.PrivateLib().opener.open(request)
        web_src = response.read().decode("UTF-8", "ignore")

        # mate illust name
        illustNamePattern = re.compile(pllc.illustNameRegex, re.S)
        self.illustName = re.findall(illustNamePattern, web_src)[0][18:][:-1]

        # mate images name
        imagesNamePattern = re.compile(pllc.imagesNameRegex, re.S)
        origName = re.findall(imagesNamePattern, web_src)
        self.imagesName = origName[1:21]

        # mate id and max count parse
        pattern = re.compile(pllc.illustAWCntRegex(self.illustInputID), re.S)
        dataCapture = re.findall(pattern, web_src)

        # cut count from include parse
        nbrPattern = re.compile(pllc.nbrRegex, re.S)
        nbrMate = re.findall(nbrPattern, dataCapture[0])
        maxCnt = string.atoi(nbrMate[1])                            # nbrMate[0] is input id, nbrMate[1] is max count

        # input want image count
        capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                + 'enter you want to crawl image count(must <= %d, ever page 20 images): ' % maxCnt))
        # count error
        while (capCnt > maxCnt) or (capCnt <= 0):
            capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                        + 'error, input count must <= %d and not 0: ' % maxCnt))
        logContext = "check gather illustrator id:" + self.illustInputID + " image(s):%d" % capCnt
        priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)

        return capCnt

    # craw illust artwork count
    @staticmethod
    def CrawlAllTargetURL(self, array, logPath):
        # page request regular:
        # no.1 referer: &type=all request url: &type=all&p=2
        # no.2 referer: &type=all&p=2 request url: &type=all&p=3
        # no.3 referer: &type=all&p=3 request url: &type=all&p=4
        # ...
        page1urlTarget = pllc.mainPage + self.illustInputID + pllc.mainPagemiddle
        if array == 1:
            urlTarget = page1urlTarget
            referer = page1urlTarget
        elif array == 2:
            urlTarget = page1urlTarget + pllc.mainPagetail + str(array)
            referer = page1urlTarget
        else:
            urlTarget = page1urlTarget + pllc.mainPagetail + str(array)
            referer = page1urlTarget + pllc.mainPagetail + str(array - 1)
        mainPageHeader = pllc.MainpageRequestHeaders(referer)
        request = urllib2.Request(url=urlTarget, headers=mainPageHeader)

        # build and install opener
        cookieHandler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
        opener = urllib2.build_opener(cookieHandler)
        urllib2.install_opener(opener)
        # open webpage, get web src, try two way
        ## response = opener.open(request)
        response = urllib2.urlopen(request, timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = "mainpage %d response successed" % array
        else:
            logContext = "mainpage %d response timeout, failed" % array
            exit()                                                  # response fail, exit program
        priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)

        web_src = response.read().decode("UTF-8", "ignore")
        pattern = re.compile(pllc.imgThumbnailRegex, re.S)          # use regex, find dailyRank art works messages
        urlCapture = re.findall(pattern, web_src)[1:21]             # findall return a tuple include 5 members

        return urlCapture

    @staticmethod
    def PackAllPageURL(self, nbr, logPath):
        # calcus nbr need request count
        if nbr <= 20:
            needPagecnt = 1                                         # nbr <= 20, request once
        else:
            needPagecnt = (nbr / 20) + 1                            # calcus need request count

        # request all url
        allURLcollection = []
        for i in range(needPagecnt):
            allURLcollection += self.CrawlAllTargetURL(self, i + 1, logPath)

        nbrPattern = re.compile(pllc.nbrRegex, re.S)                # cut artwork id list

        artworkIDs = []                                             # images id list
        imgOriginalhttps = []                                       # image original page url
        self.basePages = []                                         # image basic page
        for i in allURLcollection[:nbr]:
            vaildWord = i[-47:-18]                                  # cut vaild words
            # init to png, then will change jpg
            build_http = pllc.imgOriginalheader + vaildWord + pllc.imgOriginaltail
            # build basic page use to request image
            img_id = re.findall(nbrPattern, vaildWord)[6]           # no.6 member is id
            basePage = pllc.baseWebURL + img_id
            artworkIDs.append(img_id)                               # image id list
            imgOriginalhttps.append(build_http)                     # image url list
            self.basePages.append(basePage)                         # basic page list

        # log images info
        logContext = 'illuster: ' + self.illustName + ' id: ' + self.illustInputID + ' artworks info====>'
        priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)
        for k, i in enumerate(self.imagesName[:nbr]):
            logContext = 'no.%d image: %s id: %s url: %s' % (k, i, artworkIDs[k], imgOriginalhttps[k])
            priv_lib.PrivateLib().LogCrawlerWork(logPath, logContext)

        return imgOriginalhttps

    def iraStartCrawler(self):
        # collect essential info
        logFilePath = self.GetInputEssentialInfo(self)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        priv_lib.PrivateLib().CrawlerSignIn(logFilePath)
        # get capture image count
        crawCnt = self.GatherIndexInfo(self, logFilePath)
        urls = self.PackAllPageURL(self, crawCnt, logFilePath)
        # save images
        priv_lib.PrivateLib().SaveImageBinData(urls, self.basePages, self.workdir, logFilePath)
        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        priv_lib.PrivateLib().LogCrawlerWork(logFilePath, logContext)
        # finish
        priv_lib.PrivateLib().crawlerFinishWork(logFilePath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
