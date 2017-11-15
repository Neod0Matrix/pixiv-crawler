#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# this test script is written to scrapy Pixiv top 100 image or comic
# code by </MATRIX>@Neod Anderjon
# =====================================================================

import urllib, urllib2, cookielib, re, os, json                     # crawler depends
import logging                                                      # log record
import pllc                                                         # messages

# create a class for url response
class MainProcess:
    # class include init process
    def __init__(self):
        # request sheet
        self.loginURL = pllc.hostWebURL                              # pixiv login page
        # javascript console's headers dict
        # only use in linux's google chrome
        self.loginHeader = pllc.loginDataHeader
        # use post way to request service
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo))
        # get local cookie, create a opener for pixiv class
        self.cookie = cookielib.LWPCookieJar()                      # use last sheet to create a cookie-module
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler)

    # create a file directory to save pictures
    def MkDir(self):
        pllc.SetOSHomeFolder()
        # create a folder to save picture
        if not os.path.exists(pllc.privateFolder):
            os.makedirs(pllc.privateFolder)
            print pllc.SHELLHEAD + 'folder create successed'
            logging.info(pllc.SHELLHEAD + 'folder create successed')
        else:
            print pllc.SHELLHEAD + 'the folder has already existed'
            logging.info(pllc.SHELLHEAD + 'the folder has already existed')
        logging.basicConfig(filename = pllc.logFilePath, level = logging.DEBUG)  # save log
        print pllc.SHELLHEAD + 'this python auto-crawler work to crawle pixiv website daily top %d images' % pllc.imageCrawleNbr
        logging.info(pllc.SHELLHEAD + 'this python auto-crawler work to crawle pixiv website daily top %d images' % pllc.imageCrawleNbr)
        return pllc.privateFolder

    # first try to request website link
    def GetFirstPage(self):
        # request to server, include url, headers, sheet, request way is post
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeader)
        # use new created opener(include cookies) to open, return server response sheet
        response = self.opener.open(request)
        content = response.read().decode('utf-8')                   # read it, and decode with UTF-8
        if response.getcode() == pllc.reqSuccessCode:               # http request situation code, ok is 200
            print pllc.SHELLHEAD + 'website response successed'
            logging.info(pllc.SHELLHEAD + 'website response successed')
        else:
            print pllc.SHELLHEAD + 'website response fatal, return code %d' % response.getcode()
            logging.info(pllc.SHELLHEAD + 'website response fatal, return code %d' % response.getcode())
        return content

    # run into dailyRank page
    def GetDailyRankList(self):
        rank_url = pllc.rankWebURL                            # daily rank url
        request = urllib2.Request(rank_url)
        response = self.opener.open(request)
        content = response.read().decode('UTF-8')                   # read it, and decode with UTF-8

        ## print response.getcode()
        pattern = re.compile(pllc.rankURLRegex, re.S)                 # use regex, find dailyRank art works messages
        items = re.findall(pattern, content)                        # findall return a tuple include 5 members

        # print it to check
        for item in items:
            print item[0], item[1], item[2], item[3], item[4]
            logging.info(item[0], item[1], item[2], item[3], item[4])
        print pllc.SHELLHEAD + 'daily-rank page request successed, get the info of pictures and authors'
        logging.info(pllc.SHELLHEAD + 'daily-rank page request successed, get the info of pictures and authors')
        return items

    # write top info to a text file
    def SaveInfo(self, items):
        infos = 'top ' + str(pllc.imageCrawleNbr) + ' messages:\n'
        for item in items[:50]:                                     # findall class max get 50 memebr from list
            infos += '------------no.%s-----------\n' % item[0]
            infos += 'name: %s\nauthor: %s\nid: %s\n' % (item[1], item[2], item[4])
        # save info in a text
        with open(pllc.illustInfoFilePath, 'w') as text:
            text.write(infos.encode('UTF-8'))

    # get the page url
    def GetImagePage(self):
        illust_id = [item[4] for item in self.GetDailyRankList()]   # item[4] is author_id
        img_pages = [pllc.baseWebURL + str(i) for i in illust_id]     # every picture url address: base_url address + picture_id
        return img_pages                                            # get original image page

    # get the pages urls
    def GetImageURLs(self, img_pages):
        img_urls = []                                               # create a list to storage urls, init to empty
        # ergodic all id page, first 100
        for index, url in enumerate(img_pages[:pllc.imageCrawleNbr]): # select download picture number
            # print url # every url of id page
            print pllc.SHELLHEAD + 'locking no.%d picture page' % (index + 1) # index is 0-49, add 1 to be a 1 first index
            request = urllib2.Request(url)                          # request a response url
            response = self.opener.open(request)                    # get original image page source code
            content = response.read().decode('UTF-8')               # decode to utf-8

            # (.*?) is short mate regex
            # first use thumbnail regex to match thumbnail, then make the original with thumbnail
            # target: original illust image, others not
            try:
                pattern = re.compile(pllc.imgThumbnailRegex, re.S)
                # img = re.search(pattern, content) # find in server inspect
                img_https = pattern.findall(content)[3][10:-1]      # cut to get a https address
                img_http = img_https[0:4] + img_https[4:]           # cut to get a http address

                img_original_http = 'https://i.pximg.net/img-original/img' \
                                + img_http[44:-18] + '_p0.png'      # default is png, then process jpg format
                # check match result
                print pllc.SHELLHEAD + 'no.%d picture web address: ' % (index + 1) + img_original_http
                print pllc.SHELLHEAD + 'author pixiv id: ' + img_original_http[-15:-7] # only print id
                logging.info(pllc.SHELLHEAD + 'no.%d picture web address: ' % (index + 1) + img_original_http)
                logging.info(pllc.SHELLHEAD + 'author pixiv id: ' + img_original_http[-15:-7])

            # I don't suggest get manga, so I forbidden it
            except AttributeError:                                  # turn to manga comic, jump
                img_original_http = ''                              # set to empty, jump
                print pllc.SHELLHEAD + 'this maybe a manga comic, jump out'
                logging.info(pllc.SHELLHEAD + 'this maybe a manga comic, jump out')

            img_urls.append(img_original_http)                      # put into a list
        return img_urls
# ============================================================================================================ #
# ============================================================================================================ #

    # save get images
    def SaveImageData(self, img_urls, img_pages, path):
        for i, img_url in enumerate(img_urls):
            ## login_data = urllib.urlencode(pllc.post_data)
            ## json_login_data = json.dumps(login_data)

            # linux's chrome
            img_headers = {
                'Accept': "image/webp,image/*,*/*;q=0.8",
                'Accept-Encoding': "gzip, deflate, sdch",
                'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
                'Connection': "keep-alive",
                # 'Host': img_url[8:9] + '.pixiv.net', # host from last web page
                # must add referer, or server will return a damn http error 403, 404
                # copy from javascript console network request headers of image
                'Referer': img_pages[i],
                'User-Agent': pllc.useragentForLinuxBrowser,         # stable for linux chrome
            }
            # use GET way to request server
            ## img_url_get_way = img_url + "?" + urllib.urlencode(pllc.get_way_info)
            # make a request
            # if you want the original, the request url should be like "http://i2.pixiv.net/img-original/img/2015/04/04/00/30/41/49642237_p0.jpg"
            img_request = urllib2.Request(
                url = img_url,                                      # img_http
                ## data = json_login_data,                          # login cookie
                headers = img_headers
            )
            img_type_flag = 0                                       # replace png format

            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
            urllib2.install_opener(opener)                          # must install new created opener

            ## start_time = time.time()                                # log run time

            try:
                img_response = urllib2.urlopen(img_request, timeout = 30)
            except Exception, error:
                img_type_flag += 1                                  # replace jpg format
                print pllc.SHELLHEAD + "this image maybe a manga comic or a jpg image"
                logging.info(pllc.SHELLHEAD + "this image maybe a manga comic or a jpg image")

                ## print str(error)                                 # http error 404
                img_request = urllib2.Request(
                    url = img_url[0:-3] + 'jpg',                    # img_http
                    ## data = json_login_data,                      # login cookie
                    headers = img_headers
                )
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
                urllib2.install_opener(opener)                      # must install new created opener
                img_response = urllib2.urlopen(img_request, timeout = 30)

                if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                    print pllc.SHELLHEAD + 'get target image ok'
                    logging.info(pllc.SHELLHEAD + 'get target image ok')

                    # image has two format: jpg
                    with open(path + '/' + str(i) + '.jpg', 'wb') as jpg:
                        jpg.write(img_response.read())              # do not decode
                        print pllc.SHELLHEAD + 'save no.%d image' % i
                        logging.info(pllc.SHELLHEAD + 'save no.%d image' % i)

            ## print 'Image response code: %d' % img_response.getcode()

            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
                print pllc.SHELLHEAD + 'get target image ok'
                logging.info(pllc.SHELLHEAD + 'get target image ok')

                # image has two format: png
                with open(path + '/' + str(i) + '.png', 'wb') as png:
                    png.write(img_response.read())                  # do not decode
                    print pllc.SHELLHEAD + 'save no.%d image' % i
                    logging.info(pllc.SHELLHEAD + 'save no.%d image' % i)

            # log save picture time
            ## end_time = time.time()
            ## print pllc.pclhs + 'Elaspsed time: %f ms' % (end_time - start_time) * 1000
# ============================================================================================================ #
# ============================================================================================================ #

    # execute fuction:
    # create a folder to storage data and set to work-directory
    # try to get daily-rank page data
    # get the target list
    # get the image page
    # get the image urls
    # save top info
    # save image
    # open the storage directory with filemanager
    def StartCrawlerWork(self):
        projectPath = self.MkDir()
        self.GetFirstPage()
        rankListItems = self.GetDailyRankList()
        imageWebPages = self.GetImagePage()
        imageWebURLs = self.GetImageURLs(imageWebPages)
        self.SaveInfo(rankListItems)
        self.SaveImageData(imageWebURLs, imageWebPages, projectPath)
        # open filebox to watch result
        if pllc.os_name == 'posix':
            os.system(pllc.fileManager + ' ' + pllc.homeFolder)

if __name__ == '__main__':
    MainProcess().StartCrawlerWork()                                # use last class

print                                                               # print a empty row
print pllc.SHELLHEAD + 'log finished time: ' + pllc.excFinishTime   # log finished time
print 'copyright @' + pllc.__laboratory__ + ' technology support'
print 'code by ' + pllc.__organization__ + '@' + pllc.__author__    # print private logo
print pllc.__version__                                              # print version string

# =====================================================================
# code by </MATRIX>@Neod Anderjon
