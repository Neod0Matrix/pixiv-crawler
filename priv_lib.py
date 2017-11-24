#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to create a private library use in this crawler

import urllib2, cookielib, os, requests, urllib                     # crawler depends
import time, random
import pllc                                                         # messages
from bs4 import BeautifulSoup

pllc.EncodeDecodeResolve()

# create a class for pixiv dailyRank top
class PrivateLib:
    # help page
    """
        #################################################################################
        #    Code by </MATRIX>@Neod Anderjon(LeaderN)                                   #
        #    MatPixivCrawler Help Page                                                  #
        #    1.drt  ---     dailyRankTop, crawl Pixiv daily-rank top N artwork(s)       #
        #    2.ira  ---     illustRepoAll, crawl Pixiv any illustrator all artwork(s)   #
        #    help   ---     print this help page                                        #
        #################################################################################
    """
    def __init__(self):
        """
            class init and create some self var
            here build a sample opener
        """
        # login use url, post way data, headers
        self.loginURL = pllc.originHost
        self.postData = pllc.postData
        self.loginHeader = pllc.InitLoginHeaders()
        # example for private opener build
        self.cookie = cookielib.LWPCookieJar()                      # create a cookie words
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie) # add http cookie words
        self.opener = urllib2.build_opener(self.cookieHandler)      # build the opener
        ## self.opener.addheaders = self.loginHeader
        urllib2.install_opener(self.opener)                         # install it
        self.proxy = self.ProxyServerCrawl()                        # choose a proxy server

    @staticmethod
    def LogCrawlerWork(logPath, logInfo):
        """
            universal work log save
            its save path define in pllc.py and use here
            :param logPath: log save path
            :param logInfo: log save content
            :return:        none
        """
        # this log file must be a new file
        logFile = open(logPath, 'a+')                               # add context to file option 'a+'
        print pllc.SHELLHEAD + logInfo                              # with shell header
        print >> logFile, pllc.SHELLHEAD + logInfo                  # write to log

    def MkDir(self, logPath, folder):
        """
            create a crawler work directory
            :param logPath: log save path
            :param folder:  folder create path
            :return:        folder create path
        """
        # create a folder to save picture
        isFolderExisted = os.path.exists(folder)
        if not isFolderExisted:
            os.makedirs(folder)
            logContext = 'folder create successed'
        else:
            logContext = 'the folder has already existed'
        # remove old log file
        if os.path.exists(logPath):
            os.remove(logPath)
        self.LogCrawlerWork(logPath, logContext)

        return folder

    def CamouflageLogin(self, logPath):
        """
            camouflage browser to login
            :param logPath: log save path
            :return:        none
        """
        # login init need to commit post data to Pixiv
        request = urllib2.Request(self.loginURL, pllc.postData, self.loginHeader)
        response = self.opener.open(request)
        # try to test website response
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'login response successed'
        else:
            # response failed, you need to check network status
            logContext = 'login response fatal, return code %d' % response.getcode()
        self.LogCrawlerWork(logPath, logContext)
        web_src = response.read().decode("UTF-8", "ignore")
        print web_src

    @staticmethod
    def ProxyServerCrawl():
        """
            catch a proxy server when crwaler crawl many times website forbidden host ip
        :return:        proxy server ip dict
        """
        req_ps_url = 'http://www.xicidaili.com/nn/'
        psHeaders = {}
        if os.name == 'posix':
            psHeaders = {'User-Agent': pllc.userAgentLinux}
        elif os.name == 'nt':
            psHeaders = {'User-Agent': pllc.userAgentWindows}
        request = urllib2.Request(url=req_ps_url,
                                  headers=psHeaders)
        response = urllib2.urlopen(request, timeout=300)
        proxyRawwords = []
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'crawl proxy successed'
            web_src = response.read().decode("UTF-8", "ignore")
            # use beautifulsoup lib mate 'tr' word
            proxyRawwords = BeautifulSoup(web_src, 'lxml').find_all(pllc.proxyServerRegex)
        else:
            logContext = 'crawl proxy failed, return code: %d' %response.getcode()
        print logContext
        ip_list = []
        for i in range(1, len(proxyRawwords)):
            ip_info = proxyRawwords[i]
            tds = ip_info.find_all(pllc.arrangeProxyServerRegex)
            ip_list.append(tds[1].text + ':' + tds[2].text)

        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)                        # random catch a proxy
        proxyServer = {'http': proxy_ip}                            # setting proxy server
        print 'choose proxy server: ' + proxy_ip

        return proxyServer

    def SaveImageBinData(self, img_urls, base_pages, imgPath, logPath):
        """
            download target image(s)
            :param img_urls:    image urls list
            :param base_pages:  referer basic pages list
            :param imgPath:     image save path
            :param logPath:     log save path
            :return:            none
        """
        logContext = 'start to download target======>'
        self.LogCrawlerWork(logPath, logContext)

        for i, img_url in enumerate(img_urls):
            img_headers = pllc.OriginalImageRequestHeaders(base_pages[i]) # reset headers with basic pages
            # use GET way to request server
            ## img_url_get_way = img_url + "?" + urllib.urlencode(pllc.get_way_info)
            img_request = urllib2.Request(url=img_url,
                                          headers=img_headers)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            ## opener.addheaders = img_headers
            urllib2.install_opener(opener)                          # must install new created opener

            # pixiv website image format have jpg and png two format
            img_type_flag = 0                                       # replace png format, reset last
            img_id = img_url[57:][:-7]                              # cut id from url
            image_name = str(i) + '-' + img_id                      # image name, pixiv image name img_id + '_p0'
            try:
                img_response = urllib2.urlopen(img_request, timeout=300)
                ## img_response = opener.open(img_url, timeout=300)
            # http error because only use png format to build url
            # after except error, url will be changed to jpg format
            except Exception, e:
                logContext = str(e) + ", image format need to change"
                self.LogCrawlerWork(logPath, logContext)
                img_type_flag += 1
                chajpgurl = img_url[0:-3] + 'jpg'                   # replace to jpg format
                img_request = urllib2.Request(
                    url=chajpgurl,
                    headers=img_headers
                )
                # rebuild opener
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                ## opener.addheaders = img_headers
                urllib2.install_opener(opener)                      # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout=300) # request timeout set longer
                ## img_response = opener.open(img_url, timeout=300)

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    logContext = 'capture target jpg image ok'
                    self.LogCrawlerWork(logPath, logContext)
                    with open(imgPath + '/' + image_name + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())
                    logContext = 'download no.%d image finished' % i
                    self.LogCrawlerWork(logPath, logContext)

            # no http error, image is png format, continue request
            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                logContext = 'capture target png image ok'
                self.LogCrawlerWork(logPath, logContext)
                with open(imgPath + '/' + image_name + '.png', 'wb') as png:
                    png.write(img_response.read())
                logContext = 'download no.%d image finished' % i
                self.LogCrawlerWork(logPath, logContext)

    def crawlerFinishWork(self, logPath):
        """
            work finished log
            :param logPath: log save path
            :return:        none
        """
        rtc = time.localtime()
        ymdhms = '%d-%d-%d %d:%d:%d' % (rtc[0], rtc[1], rtc[2], rtc[3], rtc[4], rtc[5])
        logContext = "crawler work finished, log time: " + ymdhms
        self.LogCrawlerWork(logPath, logContext)
        logContext = \
            pllc.__laboratory__ + ' ' + pllc.__organization__   \
            + ' technology support\n'                                           \
            'Code by ' + pllc.__organization__ + '@' + pllc.__author__
        self.LogCrawlerWork(logPath, logContext)
        os.system(pllc.OSFileManager() + ' ' + pllc.workDir)        # open file-manager to check result

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
