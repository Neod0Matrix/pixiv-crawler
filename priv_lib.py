#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to create a private library use in this crawler

import urllib, urllib2, cookielib, os
import time, random, re
import pllc
from bs4 import BeautifulSoup
import threading
from PIL import Image
from collections import OrderedDict

pllc.encode_resolve()

class Matrix:
    """
        #########################################################################################################
        #    ██████╗ ██╗██╗  ██╗██╗██╗   ██╗       ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗     #
        #    ██╔══██╗██║╚██╗██╔╝██║██║   ██║      ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗    #
        #    ██████╔╝██║ ╚███╔╝ ██║██║   ██║█████╗██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝    #
        #    ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝╚════╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗    #
        #    ██║     ██║██╔╝ ██╗██║ ╚████╔╝       ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║    #
        #    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝         ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝    #
        #                                                                                                       #
        #    Copyright (c) 2017 @T.WKVER </MATRIX> Neod Anderjon(LeaderN)                                       #
        #    Version: 5.2.0 LTE                                                                                 #
        #    Code by </MATRIX>@Neod Anderjon(LeaderN)                                                           #
        #    MatPixivCrawler Help Page                                                                          #
        #    1.rtn  ---     RankTopN, crawl Pixiv daily/weekly/month rank top N artwork(s)                      #
        #    2.ira  ---     illustRepoAll, crawl Pixiv any illustrator all artwork(s)                           #
        #    help   ---     print this help page                                                                #
        #########################################################################################################
    """
    def __init__(self):
        # from first login save cookie and create global opener
        self.cookie = cookielib.LWPCookieJar()                      # create a cookie words
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie) # add http cookie words
        self.opener = urllib2.build_opener(self.cookieHandler)      # build the opener
        urllib2.install_opener(self.opener)

    @staticmethod
    def logprowork(logpath, savecontent):
        """
            universal work log save
            :param logpath: log save path
            :param savecontent: log save content
            :return:        none
        """
        # this log file must be a new file
        logFile = open(logpath, 'a+')                               # add context to file option 'a+'
        print pllc.SHELLHEAD + savecontent                              # with shell header
        print >> logFile, pllc.SHELLHEAD + savecontent                  # write to log

    def mkworkdir(self, logpath, folder):
        """
            create a crawler work directory
            :param self:    self class
            :param logpath: log save path
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
        if os.path.exists(logpath):
            os.remove(logpath)
        # this step will create a new log file
        self.logprowork(logpath, logContext)

        return folder

    def getproxyserver(self, logpath):
        """
            catch a proxy server when crwaler crawl many times website forbidden host ip
        :param logpath: log save path
        :return:        proxy server ip dict
        """
        req_ps_url = pllc.proxyServerRequestURL
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
            logContext = 'crawl proxy failed, return code: %d' % response.getcode()
        self.logprowork(logpath, logContext)
        ip_list = []
        for i in range(1, len(proxyRawwords)):
            ip_info = proxyRawwords[i]
            tds = ip_info.find_all(pllc.arrangeProxyServerRegex)
            # build a format: ip:port
            ip_list.append('http://' + tds[1].text + ':' + tds[2].text)

        proxy_ip = random.choice(ip_list)                           # random choose a proxy
        proxyServer = {'http': proxy_ip}                            # setting proxy server
        logContext = 'choose proxy server: ' + proxy_ip
        self.logprowork(logpath, logContext)

        return proxyServer

    def gatherpostkey(self, logpath):
        """
            POST way login need post-key
            :return:    post way request data
        """
        # request a post key
        response = self.opener.open(pllc.postKeyGeturl, timeout=300)
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'post-key response successed'
        else:
            logContext = 'post-key response failed, return code: %d' % response.getcode()
        self.logprowork(logpath, logContext)
        # cookie check
        for item in self.cookie:
            logContext = 'cookie: [name:' + item.name + '-value:' + item.value + ']'
            self.logprowork(logpath, logContext)
        # mate post key
        web_src = response.read().decode("UTF-8", "ignore")
        postPattern = re.compile(pllc.postKeyRegex, re.S)
        postKey = re.findall(postPattern, web_src)[0]
        logContext = 'get post-key: ' + postKey
        self.logprowork(logpath, logContext)

        # build basic dict
        postTabledict = OrderedDict()                               # this post data must has a order
        postTabledict['pixiv_id'] = pllc.login_data[0]
        postTabledict['password'] = pllc.login_data[1]
        postTabledict['captcha'] = ""
        postTabledict['g_recaptcha_response'] = ""
        postTabledict['post_key'] = postKey
        postTabledict['source'] = "pc"
        postTabledict['ref'] = pllc.login_ref
        postTabledict['return_to'] = pllc.hostWebURL
        # transfer to json data format
        post_data = urllib.urlencode(postTabledict).encode("UTF-8")

        return post_data

    def camouflage_login(self, logpath):
        """
            camouflage browser to login
            :param logpath: log save path
            :return:        none
        """
        # login init need to commit post data to Pixiv
        postData = self.gatherpostkey(logpath)                      # get post-key and build post-data
        response = self.opener.open(fullurl=pllc.originHost,
                                    data=postData,
                                    timeout=300)
        # try to test website response
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'login response successed'
        else:
            logContext = 'login response fatal, return code %d' % response.getcode()
        self.logprowork(logpath, logContext)

    def save_test_html(self, workdir, content, logpath):
        htmlfile = open(workdir + '/test.html', "wb")
        htmlfile.write(content)
        htmlfile.close()
        logContext = 'save request html page ok'
        self.logprowork(logpath, logContext)

    def requestpack(self, mode, url, headers, timeout):
        """
            package a request with two mode, use to test
            test result: mode 1 slower, mode 2 faster
            :param mode:        mode choose, 1 or 2
            :param url:         request url address
            :param headers:     add headers
            :param timeout:     request timeout
            :return:            response frame
        """
        response = None
        if mode == 1:
            list_headers = pllc.dict_transto_list(headers)               # change headers data type(opener use list, urlopen use dict)
            self.opener.addheaders = list_headers                       # add headers to opener
            urllib2.install_opener(self.opener)                         # must install new
            response = self.opener.open(fullurl=url, timeout=timeout)
        elif mode == 2:
            request = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(request, timeout=timeout)
        else:
            pass

        return response                                                 # call it

    def save_oneimage(self, i, img_url, base_pages, img_path, logpath):
        """
            download one target image, then multi-process will call here
            :param i:           image index
            :param img_url:     image urls list
            :param base_pages:  referer basic pages list
            :param img_path:     image save path
            :param logpath:     log save path
            :return:            none
        """
        request_mode = 2                                            # set request images mode

        # set images download arguments
        img_type_flag = 0                                           # replace png format, reset last
        img_id = img_url[57:][:-7]                                  # cut id from url
        ## image_name = str(i + 1) + '-' + img_id
        image_name = img_id

        img_headers = pllc.build_original_headers(base_pages[i])           # setting headers
        try:
            img_response = self.requestpack(request_mode, img_url, img_headers, 300)
        # http error because only use png format to build url
        # after except error, url will be changed to jpg format
        except Exception, e:
            # this error display can release
            logContext = str(e)
            self.logprowork(logpath, logContext)

            img_type_flag += 1
            changeToJPGurl = img_url[0:-3] + 'jpg'                  # replace to jpg format
            img_response = self.requestpack(request_mode, changeToJPGurl, img_headers, 300)
            if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 1:
                logContext = 'capture target no.%d jpg image ok' % (i + 1)
                self.logprowork(logpath, logContext)
                with open(img_path + '/' + image_name + '.jpg', 'wb') as jpg:
                    jpg.write(img_response.read())
                logContext = 'download no.%d image finished' % (i + 1)
                self.logprowork(logpath, logContext)

        # no http error, image is png format, continue request
        if img_response.getcode() == pllc.reqSuccessCode and img_type_flag == 0:
            logContext = 'capture target no.%d png image ok' % (i + 1)
            self.logprowork(logpath, logContext)
            with open(img_path + '/' + image_name + '.png', 'wb') as png:
                png.write(img_response.read())
            logContext = 'download no.%d image finished' % (i + 1)
            self.logprowork(logpath, logContext)

    class MultiThread(threading.Thread):
        """
            overrides its run method by inheriting the Thread class
            this class can be placed outside the main class, you can also put inside
            threads are the smallest unit of program execution flow that is less burdensome than process creation
        """
        def __init__(self, lock, i, img_url, base_pages, imgPath, logPath):
            """
                commit class arguments
                :param lock:        object lock
                :param i:           image index
                :param img_url:     image url
                :param base_pages:  referer basic page
                :param imgPath:     image save path
                :param logPath:     log save path
            """
            # callable class init
            threading.Thread.__init__(self)
            # arguments transfer to global
            self.lock = lock
            self.i = i
            self.img_url = img_url
            self.base_pages = base_pages
            self.imgPath = imgPath
            self.logPath = logPath

        def run(self):
            """
                overwrite threading.thread run() method
            :return:    none
            """
            # cancel lock release will let multi-process change to easy process
            ## self.lock.acquire()
            Matrix().save_oneimage(self.i, self.img_url, self.base_pages, self.imgPath, self.logPath)
            ## self.lock.release()

    def download_alltarget(self, urls, base_pages, workdir, logpath):
        """
            multi-process download all image
            test speed: daily-rank top 50 whole crawl elapsed time 1min
            :param urls:        all original images urls
            :param base_pages:   all referer basic pages
            :param workdir:     work directory
            :param logpath:     log save path
            :return:            none
        """
        logContext = 'start to download target(s)======>'
        self.logprowork(logpath, logContext)

        lock = threading.Lock()                                     # object lock
        for i, img_url in enumerate(urls):
            # easy process run
            ## self.save_oneimage(i, img_url, basePages, workdir, logpath)

            # create overwrite threading.Thread object
            subprocess = self.MultiThread(lock, i, img_url, base_pages, workdir, logpath)
            subprocess.setDaemon(False)                             # set every download sub-process is non-daemon process
            subprocess.start()                                      # start download
            ## subprocess.join()                                       # block sub-process, it may turn to easy process
        # parent process wait all sub-process end
        aliveThreadCnt = threading.active_count()
        while aliveThreadCnt != 1:                                  # finally only parent process
            time.sleep(3)
            aliveThreadCnt = threading.active_count()               # update count
            # display currently remaining process count
            logContext = 'currently remaining sub-thread(s): %d/%d' % (aliveThreadCnt - 1, len(urls))
            self.logprowork(logpath, logContext)
        logContext = 'all of threads reclaim, download finished=====>'
        self.logprowork(logpath, logContext)

    def htmlpreview_build(self, workdir, htmlpath, logpath):
        """
            build a html file to browse image
            :param self:        class self
            :param workdir:     work directory
            :param htmlpath:    html file save path
            :param logpath:     log save path
            :return:            none
        """
        htmlFile = open(htmlpath, "wb")                             # write html file
        # build html background page text
        htmlFile.writelines("<html>\r\n<head>\r\n<title>pixiv-crawler(MatPixivCrawler) ResultPage</title>\r\n</head>\r\n<body>\r\n")
        htmlFile.writelines("<script>window.onload = function(){"
                            "var imgs = document.getElementsByTagName('img');"
                            "for(var i = 0; i < imgs.length; i++){"
                            "imgs[i].onclick = function(){"
                            "if(this.width == this.attributes['oriWidth'].value && this.height == this.attributes['oriHeight'].value){"
                            "this.width = this.attributes['oriWidth'].value * 1.0 / this.attributes['oriHeight'].value * 200;"
                            "this.height = 200;"
                            "}else{this.width = this.attributes['oriWidth'].value ;"
                            "this.height = this.attributes['oriHeight'].value;}}}};</script>")
        for i in os.listdir(workdir):
            if i[-4:len(i)] in [".png", ".jpg", ".bmp"]:            # support image format
                filename = i
                # this step must protect image download end, or will get a IOError
                try:
                    width, height = Image.open(workdir + '\\' + filename).size
                except Exception, e:
                    logContext = str(e) + "read image file error, jump out"
                    self.logprowork(logpath, logContext)
                    time.sleep(5)                                   # wait download sub-process end
                    width, height = Image.open(workdir + '\\' + filename).size
                filename = filename.replace("#", "%23")
                ## htmlFile.writelines("<a href = \"%s\">"%("./" + filename))
                # set image source line
                htmlFile.writelines(
                    "<img src = \"%s\" width = \"%dpx\" height = \"%dpx\" oriWidth = %d oriHeight = %d />\r\n"
                    % ("./" + filename, width * 1.0 / height * 200, 200, width, height)) # limit display images size
                ## htmlFile.writelines("</a>\r\n")
        # end of htmlfile
        htmlFile.writelines("</body>\r\n</html>")
        htmlFile.close()
        logContext = 'image browse html product finished'
        self.logprowork(logpath, logContext)

    def work_finished(self, logpath):
        """
            work finished log
            :param logpath: log save path
            :return:        none
        """
        rtc = time.localtime()                                      # real log get
        ymdhms = '%d-%d-%d %d:%d:%d' % (rtc[0], rtc[1], rtc[2], rtc[3], rtc[4], rtc[5])
        logContext = "crawler work finished, log time: " + ymdhms
        self.logprowork(logpath, logContext)
        logContext =                                                    \
            pllc.__laboratory__ + ' ' + pllc.__organization__           \
            + ' technology support\n'                                   \
            'Code by ' + pllc.__organization__ + '@' + pllc.__author__
        self.logprowork(logpath, logContext)
        os.system(pllc.platform_filemanager() + ' ' + pllc.work_dir)        # open file-manager to check result

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
