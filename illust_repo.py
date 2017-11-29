#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to get a illust all repo images

import re                                                           # crawler depends
import time, string
import pllc, priv_lib                                               # local lib

pp = priv_lib.PrivateLib()
pllc.encode_resolve()

class IllustratorRepos:
    """
        every illustrator in Pixiv has own mainpage
        this class include fuction will crawl all of those page all images
    """
    def __init__(self):
        """class include init process"""
        # global illust id
        self.illustInputID = raw_input(pllc.SHELLHEAD
                + 'enter you want to crawl illuster id: ')
        # work directory create
        self.workdir = pllc.setting_platform_workdir() + self.illustInputID
        self.logpath = self.workdir + pllc.logfile_name
        self.htmlpath = self.workdir + pllc.htmlfile_name

    @staticmethod
    def gather_preloadinfo(self, logpath):
        """
            crawler need to know how many images do you want
            :param self:    self class
            :param logpath: log save path
            :return:        request images count
        """
        # get illust artwork count mainpage url
        cnt_url = pllc.mainPage + self.illustInputID
        response = pp.opener.open(fullurl=cnt_url,
                                  data=pllc.login_data[2],
                                  timeout=300)
        web_src = response.read().decode("UTF-8", "ignore")

        # mate illustrator name
        illustNamePattern = re.compile(pllc.illustNameRegex, re.S)
        self.illustName = re.findall(illustNamePattern, web_src)[0][10:][:-1]

        # mate max count
        pattern = re.compile(pllc.illustAWCntRegex, re.S)
        maxCntword = re.findall(pattern, web_src)[1][5:][:-2]
        maxCnt = string.atoi(maxCntword)

        # input want image count
        capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                + 'enter you want to crawl image count(all repo have %d, each page at most 20 images): ' % maxCnt))
        # count error
        while (capCnt > maxCnt) or (capCnt <= 0):
            capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                + 'error, input count must <= %d and not 0: ' % maxCnt))
        logContext = "check gather illustrator id:" + self.illustInputID + " image(s):%d" % capCnt
        pp.logprowork(logpath, logContext)

        return capCnt

    @staticmethod
    def crawl_onepage_data(self, array, logpath):
        """
            crawl all target url about images
            page request regular:
            no.1 referer: &type=all request url: &type=all&p=2
            no.2 referer: &type=all&p=2 request url: &type=all&p=3
            no.3 referer: &type=all&p=3 request url: &type=all&p=4
            :param self:    self class
            :param array:   count cut to every 20 images from each page, they have an array
            :param logpath: log save path
            :return:        use regex to mate web src thumbnail images url
        """
        step1url = pllc.mainPage + self.illustInputID + pllc.mainPagemiddle
        if array == 1:
            urlTarget = step1url
        elif array == 2:
            urlTarget = step1url + pllc.mainPagetail + str(array)
        else:
            urlTarget = step1url + pllc.mainPagetail + str(array)
        response = pp.opener.open(fullurl=urlTarget,
                                  data=pllc.login_data[2],
                                  timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = "mainpage %d response successed" % array
        else:
            logContext = "mainpage %d response timeout, failed" % array
        pp.logprowork(logpath, logContext)
        # each page cut thumbnail image url
        web_src = response.read().decode("UTF-8", "ignore")

        # mate artworks name
        imageNamePattern = re.compile(pllc.imagesNameRegex, re.S)
        imagesNameword = re.findall(imageNamePattern, web_src)
        imagesName = []
        for i in imagesNameword:
            imagesName.append(i[10:-1])

        # thumbnail image urls
        pattern = re.compile(pllc.mainpageThumbnailRegex, re.S)
        thumbnailImageurls = re.findall(pattern, web_src)

        logContext = "mainpage %d data gather finished" % array
        pp.logprowork(logpath, logContext)

        return thumbnailImageurls, imagesName

    @staticmethod
    def crawl_allpage_target(self, nbr, logpath):
        """
            package all gather url
            :param self:    self class
            :param nbr:     package images count
            :param logpath: log save path
            :return:        build original images urls list
        """
        # calcus nbr need request count
        if nbr <= 20:
            needPagecnt = 1                                         # nbr <= 20, request once
        else:
            needPagecnt = (nbr / 20) + 1                            # calcus need request count

        # gather all data(thumbnail images and names)
        allThumbnailimage = []
        allArtworkName = []
        for i in range(needPagecnt):
            dataCapture = self.crawl_onepage_data(self, i + 1, logpath)
            allThumbnailimage += dataCapture[0]
            allArtworkName += dataCapture[1]

        nbrPattern = re.compile(pllc.nbrRegex, re.S)                # cut artwork id list

        artworkIDs = []                                             # images id list
        imgOriginalhttps = []                                       # image original page url
        self.basePages = []                                         # image basic page
        for i in allThumbnailimage[:nbr]:
            vaildWord = i[50:][:-19]                                # cut vaild words
            # init to png, then will change jpg
            build_http = pllc.imgOriginalheader + vaildWord + pllc.imgOriginaltail
            # build basic page use to request image
            img_id = re.findall(nbrPattern, vaildWord)[6]           # no.6 member is id
            basePage = pllc.baseWebURL + img_id
            artworkIDs.append(img_id)                               # image id list
            imgOriginalhttps.append(build_http)                     # image url list
            self.basePages.append(basePage)                         # basic page list

        # log images info
        logContext = 'illustrator: ' + self.illustName + ' id: ' + self.illustInputID + ' artworks info====>'
        pp.logprowork(logpath, logContext)

        for k, i in enumerate(allArtworkName[:nbr]):
            logContext = 'no.%d image: %s id: %s url: %s' % ((k + 1), i, artworkIDs[k], imgOriginalhttps[k])
            pp.logprowork(logpath, logContext)

        return imgOriginalhttps

    def start_ira(self):
        """
            include this class run logic
            :return:    none
        """
        # make dir
        pp.mkworkdir(self.logpath, self.workdir)
        # log runtime
        starttime = time.time()
        # check website can response crawler
        pp.getproxyserver(self.logpath)
        pp.camouflage_login(self.logpath)
        # get capture image count
        target_cnt = self.gather_preloadinfo(self, self.logpath)
        urls = self.crawl_allpage_target(self, target_cnt, self.logpath)
        # save images
        pp.download_alltarget(urls, self.basePages, self.workdir, self.logpath)
        # stop log time
        endtime = time.time()
        logContext = "elapsed time: %0.2fs" % (endtime - starttime)
        pp.logprowork(self.logpath, logContext)
        # finish
        pp.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)
        pp.work_finished(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
