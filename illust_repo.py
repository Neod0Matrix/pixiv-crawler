#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to get a illust all repo images

import re
import time, string
import pllc
import priv_lib

pvmx = priv_lib.Matrix()
pllc.encode_resolve()

class IllustratorRepos(object):
    """
        every illustrator in Pixiv has own mainpage
        this class include fuction will crawl all of those page all images
    """
    def __init__(self, iid, workdir, logname, htmlname):
        """
            :param iid:         illustrator id
            :param workdir:     work directory
            :param logname:     log name
            :param htmlname:    html name
        """
        self.illustInputID = iid
        self.workdir = workdir + self.illustInputID
        self.logpath = self.workdir + logname
        self.htmlpath = self.workdir + htmlname

    def gather_preloadinfo(self, logpath):
        """
            crawler need to know how many images do you want
            :param self:    self class
            :param logpath: log save path
            :return:        request images count
        """
        # get illust artwork count mainpage url
        cnt_url = pllc.mainPage + self.illustInputID
        response = pvmx.opener.open(fullurl=cnt_url,
                                    data=pllc.login_data[2],
                                    timeout=300)
        web_src = response.read().decode("UTF-8", "ignore")

        # mate illustrator name
        illustNamePattern = re.compile(pllc.illustNameRegex, re.S)
        arthor_name = re.findall(illustNamePattern, web_src)[0][10:-1]

        # mate max count
        pattern = re.compile(pllc.illustAWCntRegex, re.S)
        maxCntword = re.findall(pattern, web_src)[1][5:-2]
        maxCnt = string.atoi(maxCntword)

        # input want image count
        capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                + 'enter you want to crawl image count(all repo have %d, each page at most 20 images): ' % maxCnt))
        # count error
        while (capCnt > maxCnt) or (capCnt <= 0):
            capCnt = string.atoi(raw_input(pllc.SHELLHEAD
                + 'error, input count must <= %d and not 0: ' % maxCnt))
        logContext = "check gather illustrator id:" + self.illustInputID + " image(s):%d" % capCnt
        pvmx.logprowork(logpath, logContext)

        return capCnt, arthor_name

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
        response = pvmx.opener.open(fullurl=urlTarget,
                                    data=pllc.login_data[2],
                                    timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = "mainpage %d response successed" % array
        else:
            logContext = "mainpage %d response timeout, failed" % array
        pvmx.logprowork(logpath, logContext)
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
        pvmx.logprowork(logpath, logContext)

        return thumbnailImageurls, imagesName

    def crawl_allpage_target(self, nbr, arthor_name, logpath):
        """
            package all gather url
            :param self:        self class
            :param nbr:         package images count
            :param arthor_name: arthor name
            :param logpath:     log save path
            :return:            build original images urls list
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
            dataCapture = self.crawl_onepage_data(i + 1, logpath)
            allThumbnailimage += dataCapture[0]
            allArtworkName += dataCapture[1]

        nbrPattern = re.compile(pllc.nbrRegex, re.S)                # cut artwork id list

        artworkIDs = []                                             # images id list
        targetURL = []                                              # image original page url
        basePages = []                                              # image basic page
        for i in allThumbnailimage[:nbr]:
            vaildWord = i[50:-19]                                   # cut vaild words
            # init to png, then will change jpg
            build_http = pllc.imgOriginalheader + vaildWord + pllc.imgOriginaltail
            # build basic page use to request image
            img_id = re.findall(nbrPattern, vaildWord)[6]           # no.6 member is id
            basePage = pllc.baseWebURL + img_id
            artworkIDs.append(img_id)                               # image id list
            targetURL.append(build_http)                            # image url list
            basePages.append(basePage)                              # basic page list

        # log images info
        logContext = 'illustrator: ' + arthor_name + ' id: ' + self.illustInputID + ' artworks info====>'
        pvmx.logprowork(logpath, logContext)

        for k, i in enumerate(allArtworkName[:nbr]):
            logContext = 'no.%d image: %s id: %s url: %s' % ((k + 1), i, artworkIDs[k], targetURL[k])
            pvmx.logprowork(logpath, logContext)

        return targetURL, basePages

    def start(self):
        """
            include this class run logic
            :return:    none
        """
        pvmx.mkworkdir(self.logpath, self.workdir)

        starttime = time.time()

        pvmx.camouflage_login(self.logpath)                         # login website, key step
        # gather info and data
        info = self.gather_preloadinfo(self.logpath)
        datas = self.crawl_allpage_target(info[0], info[1], self.logpath)
        # download images
        pvmx.download_alltarget(datas[0], datas[1], self.workdir, self.logpath)

        endtime = time.time()
        logContext = "elapsed time: %0.2fs" % (endtime - starttime)
        pvmx.logprowork(self.logpath, logContext)

        pvmx.htmlpreview_build(self.workdir, self.htmlpath, self.logpath)
        pvmx.work_finished(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
