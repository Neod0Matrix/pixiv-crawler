#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get pixiv dailyRank top images

import urllib2, cookielib, re                                       # crawler depends
import datetime, os, string
import pllc, priv_lib                                               # local lib

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
    def CrawlTargetURLList(self, img_nbr):
        logContext = 'crawl rank list======>'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        rank_url = pllc.rankWebURL
        request = urllib2.Request(rank_url)
        response = priv_lib.PrivateLib().opener.open(request)
        web_src = response.read().decode('UTF-8')                   # get webpage src

        pattern = re.compile(pllc.rankURLRegex, re.S)               # use regex, find dailyRank art works messages
        dataCapture = re.findall(pattern, web_src)                  # findall return a tuple include 5 members
        for i in dataCapture:
            print i[0], i[1], i[2], i[3], i[4]                      # list all members
        logContext =  'daily-rank page request successed, get the info of pictures and authors'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        infos = 'top ' + str(img_nbr) + ' messages:\n'
        # findall class max get 50 memebr from list
        for i in dataCapture[:img_nbr]:
            infos += '------------no.%s-----------\n' % i[0]  # artwork title
            infos += 'name: %s\nilluster: %s\nid: %s\n' % (i[1], i[2], i[4])

        # save info in a text
        with open(pllc.illustInfoFilePath, 'w+') as text:
            text.write(infos.encode('UTF-8'))

        # i[4] is illust id
        return [i[4] for i in dataCapture]

    # get the pages urls
    @staticmethod
    def BuildOriginalImageURL(self, ilu_ids, img_nbr):
        img_urls = []                                               # create a list to storage urls, init to empty

        self.basePages = [pllc.baseWebURL + str(i) for i in ilu_ids]     # every picture url address: base_url address + picture_id

        logContext = 'collect some url info======>'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        # ergodic all id page, first 100
        for index, url in enumerate(self.basePages[:img_nbr]):           # select download picture number
            # print url # every url of id page
            logContext = 'locking no.%d picture page' % index
            priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

            response = priv_lib.PrivateLib().opener.open(urllib2.Request(url)) # get original image page source code
            web_src = response.read().decode('UTF-8')               # decode to utf-8

            # use thumbnail info to get key info, then build original image url
            try:
                start_mate = 2                                      # 20171116pm2052 test value set to 2
                build_id = 0                                      # start is 0
                # because pixiv will often change website model format, use mate to get correct image
                # must have a verify way
                while build_id != ilu_ids[index]:
                    # cut to get a https address
                    img_https = re.compile(pllc.imgThumbnailRegex, re.S).findall(web_src)[start_mate][10:-1]
                    # cut to get a http address
                    img_http = img_https[0:4] + img_https[4:]
                    # default is png, after handle jpg
                    img_original_http = 'https://i.pximg.net/img-original/img' + img_http[44:-18] + '_p0.png'
                    build_id = img_original_http[-15:-7]

                    start_mate = start_mate + 1                     # continue to next element

                # check match result
                logContext = 'no.%d image web address: ' % index + img_original_http
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
                logContext = 'illust pixiv id: ' + build_id
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

            # I don't suggest get manga, so I forbidden it
            except AttributeError:                                  # turn to manga comic, jump
                img_original_http = ''                              # set to empty, jump
                logContext = 'this maybe a manga comic, jump out'
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
            img_urls.append(img_original_http)                      # put into a list

        return img_urls

    # save get images
    @staticmethod
    def SaveImageBinData(self, img_urls, path):
        logContext = 'start to download target======>'
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

        for i, img_url in enumerate(img_urls):
            if os.name == 'posix':
                img_headers = {
                    'Accept': "image/webp,image/*,*/*;q=0.8",
                    'Accept-Encoding': "gzip, deflate, sdch",
                    'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
                    'Connection': "keep-alive",
                    # 'Host': img_url[8:9] + '.pixiv.net',          # host from last web page
                    # must add referer, or server will return a damn http error 403, 404
                    # copy from javascript console network request headers of image
                    'Referer': self.basePages[i],                   # request page
                    'User-Agent': pllc.useragentForLinuxBrowser,
                }
            elif os.name == 'nt':
                img_headers = {
                    'Accept': "image/webp,image/*,*/*;q=0.8",
                    'Accept-Encoding': "gzip, deflate, sdch",
                    'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
                    'Connection': "keep-alive",
                    # 'Host': img_url[8:9] + '.pixiv.net', # host from last web page
                    # must add referer, or server will return a damn http error 403, 404
                    # copy from javascript console network request headers of image
                    'Referer': self.basePages[i],
                    'User-Agent': pllc.useragentForWindowsBrowser,
                }

            # use GET way to request server
            ## img_url_get_way = img_url + "?" + urllib.urlencode(pllc.get_way_info)
            img_request = urllib2.Request(url = img_url, headers = img_headers)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            urllib2.install_opener(opener)                          # must install new created opener

            image_name = pllc.image_header + str(i)                 # image name

            # pixiv website image format have jpg and png two format
            img_type_flag = 0                                       # replace png format, reset last
            try:
                img_response = urllib2.urlopen(img_request, timeout = 30)
            except Exception, e:
                logContext = "check http error: " + str(e)
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
                img_type_flag += 1                                  # replace jpg format
                logContext = "this image maybe a manga comic or a jpg image"
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

                img_request = urllib2.Request(
                    url = img_url[0:-3] + 'jpg',                    # img_http
                    ## data = json_login_data,                      # login cookie
                    headers = img_headers
                )
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                urllib2.install_opener(opener)                      # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout = 300) # request timeout set longer

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    logContext = 'get target image ok'
                    priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
                    # image has two format: jpg
                    with open(path + '/' + image_name + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())              # do not decode
                    logContext = 'download no.%d finished' % i
                    priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                logContext = 'get target image ok'
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

                # image has two format: png
                with open(path + '/' + image_name + '.png', 'wb') as png:
                    png.write(img_response.read())                  # do not decode
                logContext = 'download no.%d finished' % i
                priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)

    # class main call process
    def drtStartCrawler(self):
        # prepare works
        nbr = self.GetEssentialInfo(self, self.workdir, self.logpath)
        # log runtime
        starttime = datetime.datetime.now()
        # check website can response crawler
        priv_lib.PrivateLib().CrawlerSignIn(self.logpath)
        # get ids and urls
        ids = self.CrawlTargetURLList(self, nbr)
        urls = self.BuildOriginalImageURL(self, ids, nbr)
        # save images
        self.SaveImageBinData(self, urls, self.workdir)
        # stop log time
        endtime = datetime.datetime.now()
        logContext = "elapsed time: %ds" % (endtime - starttime).seconds
        priv_lib.PrivateLib().LogCrawlerWork(self.logpath, logContext)
        # finish
        priv_lib.PrivateLib().crawlerFinishWork(self.logpath)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
