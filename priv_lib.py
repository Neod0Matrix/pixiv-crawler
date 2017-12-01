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
from retrying import retry

pllc.encode_resolve()
proxyHascreated = False                                             # global var init value

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
        #    Version: 5.4.0 LTE                                                                                 #
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
        urllib2.install_opener(self.opener)                         # install it

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
            :return:        proxy server, add to opener
        """
        req_ps_url = pllc.proxyServerRequestURL
        psHeaders = {}
        if os.name == 'posix':
            psHeaders = {'User-Agent': pllc.userAgentLinux}
        elif os.name == 'nt':
            psHeaders = {'User-Agent': pllc.userAgentWindows}
        request = urllib2.Request(url=req_ps_url,
                                  headers=psHeaders)
        response = urllib2.urlopen(request, timeout=40)
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
        response = self.opener.open(pllc.postKeyGeturl, timeout=40)
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
                                    timeout=40)
        # try to test website response
        if response.getcode() == pllc.reqSuccessCode:
            logContext = 'login response successed'
        else:
            logContext = 'login response fatal, return code %d' % response.getcode()
        self.logprowork(logpath, logContext)

    def save_test_html(self, workdir, content, logpath):
        htmlfile = open(workdir + pllc.symbol + 'test.html', "wb")
        htmlfile.write(content)
        htmlfile.close()
        logContext = 'save request html page ok'
        self.logprowork(logpath, logContext)

    @retry
    def save_oneimage(self, index, url, basepages, savepath, logpath):
        """
            download one target image, then multi-process will call here
            add retry decorator, if first try failed, it will auto-retry
            :param index:       image index
            :param url:         image urls list
            :param basepages:   referer basic pages list
            :param savepath:    image save path
            :param logpath:     log save path
            :return:            none
        """
        # set images download arguments
        timeout = 30                                                # default set to 30s
        imgDatatype = 'png'                                         # default png format
        image_name = url[57:-7]                                     # cut id from url to build image name

        # preload proxy, just once
        proxy_handler = None
        global proxyHascreated
        if proxyHascreated is False:
            proxyHascreated = True
            proxy = self.getproxyserver(logpath)
            proxy_handler = urllib2.ProxyHandler(proxy)

        # setting headers
        headers = pllc.build_original_headers(basepages[index])
        list_headers = pllc.dict_transto_list(headers)
        self.opener.addheaders = list_headers
        urllib2.install_opener(self.opener)                         # must install new
        response = None

        try:
            response = self.opener.open(fullurl=url,
                                        timeout=timeout)
        # timeout or image data type error
        except urllib2.HTTPError, e:
            # this error display can release
            ## logContext = str(e.code)
            ## self.logprowork(logpath, logContext)

            # http error 404, change image type
            if e.code == pllc.reqNotFound:
                imgDatatype = 'jpg'                                 # change data type
                changeToJPGurl = url[0:-3] + imgDatatype
                try:
                    response = self.opener.open(fullurl=changeToJPGurl,
                                                timeout=timeout)
                except urllib2.HTTPError, e:
                    # this error display can release
                    ## logContext = str(e.code)
                    ## self.logprowork(logpath, logContext)

                    # not 404 change proxy
                    if e.code != pllc.reqNotFound:
                        # if timeout, use proxy reset request
                        logContext = "change proxy server"
                        self.logprowork(logpath, logContext)
                        self.opener = urllib2.build_opener(proxy_handler) # add proxy handler
                        response = self.opener.open(fullurl=changeToJPGurl,
                                                    timeout=timeout)
                    else:
                        pass
            # if timeout, use proxy reset request
            else:
                logContext = "change proxy server"
                self.logprowork(logpath, logContext)
                self.opener = urllib2.build_opener(proxy_handler)   # add proxy handler
                response = self.opener.open(fullurl=url,
                                            timeout=timeout)

        if response.getcode() == pllc.reqSuccessCode:
            # save response data to image format
            imgBindata = response.read()
            logContext = 'capture target no.%d image ok' % (index + 1)
            self.logprowork(logpath, logContext)
            # this step will delay much time
            with open(savepath + image_name + '.' + imgDatatype, 'wb') as jpg:
                jpg.write(imgBindata)
            logContext = 'download no.%d image finished' % (index + 1)
            self.logprowork(logpath, logContext)

    class MultiThreading(threading.Thread):
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

        sub_thread = None
        lock = threading.Lock()                                     # object lock
        for i, img_url in enumerate(urls):
            # create overwrite threading.Thread object
            sub_thread = self.MultiThreading(lock, i, img_url, base_pages, workdir, logpath)
            sub_thread.setDaemon(False)                             # set every download sub-process is non-daemon process
            sub_thread.start()                                      # start download
            time.sleep(0.5)                                         # confirm thread has been created
        # parent thread wait all sub-thread end
        aliveThreadCnt = threading.active_count()
        while aliveThreadCnt != 1:                                  # finally only parent process
            time.sleep(3)
            aliveThreadCnt = threading.active_count()               # update count
            # display currently remaining process count
            logContext = 'currently remaining sub-thread(s): %d/%d' % (aliveThreadCnt - 1, len(urls))
            self.logprowork(logpath, logContext)
            sub_thread.join()                                       # block parent-thread

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
                    width, height = Image.open(workdir + filename).size
                except Exception, e:
                    logContext = str(e) + "read image file error, jump out"
                    self.logprowork(logpath, logContext)
                    time.sleep(5)                                   # wait download sub-process end
                    width, height = Image.open(workdir + filename).size
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
