#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this test script is written to handle datas and some info

# projrct info
__author__          = 'Neod Anderjon(LeaderN)'                      # author signature
__laboratory__      = 'T.WKVER'                                     # lab
__organization__    = '</MATRIX>'
__version__         = 'v4p5_LTE'

import urllib2, re, urllib, json                                    # post data build
import time, os, linecache, sys                                     # name folder and files
import getpass                                                      # user and passwd input
from collections import OrderedDict

SHELLHEAD = 'MatPixivCrawler@' + __organization__ + ':~$ '          # copy linux head symbol

# ==============================================pixiv login info====================================================

def EncodeDecodeResolve():
    """
        use reload sys to resolve python damn encode question
        :return:    none
    """
    reload(sys)
    sys.setdefaultencoding('UTF-8')
EncodeDecodeResolve()                                               # run once just ok

def LoginInfoLoad():
    """
        get user input username and password
        login.cr file example:
        =================================
        [login]
        <mail>
        <passwd>
        =================================
        :return:    username, password
    """
    print '###########################[pixiv-crawler(MatPixivCrawler) %s]###########################\n' % __version__
    loginFilePath = os.getcwd() + '/' + 'login.cr'                  # get local dir path
    isLoginCrExisted = os.path.exists(loginFilePath)
    if isLoginCrExisted:
        userMailBox = linecache.getline(loginFilePath, 2)           # row 2, usernamemail
        userPassword = linecache.getline(loginFilePath, 3)          # row 3, password
        # empty file
        if userMailBox == '' or userPassword == '':
            print SHELLHEAD + "login.cr file invaild, please input your login info"
            userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
            userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ')
        else:
            check = raw_input(SHELLHEAD + "please check your info:\n"
                                          "    username: %s    password: %s"
                                          "Yes or No?: " % (userMailBox, userPassword))
            # user judge info are error
            if check != 'yes' and check != 'Yes' and check != 'YES' and check != 'y' and check != 'Y':
                print SHELLHEAD + "you can write new info"
                userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
                userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ')
    # no login.cr file
    else:
        print SHELLHEAD + "cannot find login.cr file, please input your login info"
        userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
        userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ')

    return userMailBox.strip(), userPassword.strip()                # strip() delete symbol '\n'
loginInfo = LoginInfoLoad()                                         # call once

# ========================================some use url address=====================================================
# login request must be https proxy format, request page or image must be http proxy

# login and request image https proxy
wwwHost = "www.pixiv.net"                                           # only can set into host
hostWebURL = 'https://www.pixiv.net/'
accountHost = "accounts.pixiv.net"                                  # account login
postKeyGeturl = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
login_ref = 'wwwtop_accounts_index'                                 # post data include
originHost = "https://accounts.pixiv.net/api/login?lang=en"         # login request url
originHost2 = "https://accounts.pixiv.net"                          # login origin
# request universal original image constant words
imgOriginalheader = 'https://i.pximg.net/img-original/img'          # original image https url header
imgOriginaltail = '_p0.png'                                         # original image https url tail, default set to png
# page request http proxy
proxyServerRequestURL = 'http://www.xicidaili.com/nn/'              # proxy server get website
ucRankURL = 'http://www.pixiv.net/ranking.php?mode='                # rank top universal word header
r18RankWordTail = '_r18'                                            # r18 rank word tail
dailyRankURL = ucRankURL + 'daily'                                  # daily-rank
weeklyRankURL = ucRankURL + 'weekly'                                # weekly-rank
monthlyRankURL = ucRankURL + 'monthly'                              # monthly-rank
dailyRankURL_R18 = dailyRankURL + r18RankWordTail                   # r18 daily-rank
weeklyRankURL_R18 = weeklyRankURL + r18RankWordTail                 # r18 weekly-rank
monthlyRankURL_R18 = monthlyRankURL + r18RankWordTail               # r18 monthly-rank
baseWebURL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' # basic format
illustHomeURL = 'http://www.pixiv.net/member.php?id='               # illust home page
mainPage = 'http://www.pixiv.net/member_illust.php?id='             # illust main page
mainPagemiddle = '&type=all'                                        # url middle word
mainPagetail = '&p='                                                # url tail word

# ==================================http request headers include data============================================

reqSuccessCode = 200
# login headers info dict
userAgentLinux = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                           "Chrome/56.0.2924.87 Safari/537.36"
userAgentWindows = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                            " Chrome/60.0.3112.90 Safari/537.36"
accept = "application/json, text/javascript, */*; q=0.01"
accept2 = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
acceptEncoding = "gzip, deflate, br"
acceptEncoding2 = "br"                                              # no use gzip, transfer speed down, but will not error
acceptLanguage = "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2"
cacheControl = "no-cache"
connection = "keep-alive"
contentType = "application/x-www-form-urlencoded; charset=UTF-8"
xRequestwith = "XMLHttpRequest"

def InitLoginHeaders():
    """
        first login to Pixiv, use POST way
        :return:    build headers
    """
    baseHeaders = {
        'Accept': accept,
        'Accept-Encoding': acceptEncoding,
        'Accept-Language': acceptLanguage,
        'Cache-Control': cacheControl,
        'Connection': connection,
        'Content-Length': "207",
        'Content-Type': contentType,
        'Cookie': "",                                               # cannot include
        'DNT': "1",
        'Host': accountHost,
        'Origin': originHost2,
        'Referer': postKeyGeturl,                                   # last page is request post-key page
        'X-Requested-With': xRequestwith,
    }
    buildHeaders = {}
    # linux
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())

    return buildHeaders

def R18DailyRankRequestHeaders():
    """
        r18 daily-rank page request headers
        :return:    build headers
    """
    baseHeaders = {
        'Accept': accept2,
        'Accept-Encoding': acceptEncoding,
        'Accept-Language': acceptLanguage,
        'Cache-Control': "max-age=0",
        'Connection': connection,
        'DNT': "1",
        'Host': wwwHost,
        'Referer': "https://www.pixiv.net/ranking.php?mode=daily",  # https proxy string
        'Upgrade-Insecure-Requests': "1",
    }
    buildHeaders = {}
    # linux
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())

    return buildHeaders

def MainpageRequestHeaders(referer):
    """
        illustrator private mainpage request headers
        :param referer: headers need a last page referer
        :return:        build headers
    """
    baseHeaders = {
        'Accept': accept2,
        'Accept-Encoding': acceptEncoding2,
        'Accept-Language': acceptLanguage,
        'Connection': connection,
        'DNT': 1,
        'Host': wwwHost,
        'Referer': referer,
        'Upgrade-Insecure-Requests': 1,
    }
    buildHeaders = {}
    # linux
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())

    return buildHeaders

# original image
def OriginalImageRequestHeaders(referer):
    """
        original image request headers
        :param referer: headers need a last page referer
        :return:        build headers
    """
    baseHeaders = {
        'Accept': "image/webp,image/*,*/*;q=0.8",
        'Accept-Encoding': "gzip, deflate, sdch",
        'Accept-Language': acceptLanguage,
        'Connection': connection,
        # 'Host': img_url[8:9] + '.pixiv.net',                  # host from last web page
        # must add referer, or server will return a damn http error 403, 404
        # copy from javascript console network request headers of image
        'Referer': referer,  # request basic page
    }
    buildHeaders = {}
    # linux
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())

    return buildHeaders

# =======================================regex collection==========================================================

postKeyRegex = 'key".*?"(.*?)"'                                     # mate post key
rankTitleRegex = '<section.*?data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)" data-date="(.*?)".*?data-id="(.*?)"'
rankVWRegex = 'r/img/.*?_'                                          # from dailyRank page gather vaild words
nbrRegex = '\d+\.?\d*'                                              # mate any number
imgThumbnailRegex = '<img src="(.*?)"'                              # mate thumbnail image
illustNameRegex = 'r:title" content=".*? '                          # mate illust name
imagesNameRegex = '" alt="(.*?)"'                                   # mate images name
proxyServerRegex = 'tr'                                             # use beautifulsoup module, easy
arrangeProxyServerRegex = 'td'                                      # cut gather list
# illust artwork count mate
def illustAWCntRegex(setid):
    return 'eRegister" data-user-id="%s">.*?<' % setid
# ======================================login need word build================================================
# http request have more way, Pixiv use POST way to login and request image, use GET way to request page

# GET way need info
getwayRegInfo = [('user', loginInfo[0]), ('pass', loginInfo[1])]    # priv_lib will first init it
getData = json.dumps(urllib.urlencode(getwayRegInfo))               # call once

def postKeyGather():
    """
        POST way login need post-key
        :return:    post way request data
    """
    # build basic dict
    # this post data must has a order
    postTabledict = OrderedDict()
    postTabledict['pixiv_id'] = loginInfo[0]
    postTabledict['password'] = loginInfo[1]
    postTabledict['captcha'] = ""
    postTabledict['g_recaptcha_response'] = ""

    # request a post key
    request = urllib2.Request(postKeyGeturl)
    response = urllib2.urlopen(request, timeout=300)
    # mate post key
    web_src = response.read().decode("UTF-8", "ignore")
    postPattern = re.compile(postKeyRegex, re.S)
    postKey = re.findall(postPattern, web_src)[0]
    print SHELLHEAD + 'get post-key: ' + postKey                    # display key

    # pack the dict with order
    postTabledict['post_key'] = postKey
    postTabledict['source'] = "pc"
    postTabledict['ref'] = login_ref
    postTabledict['return_to'] = hostWebURL

    # transfer to json data format
    post_data = urllib.urlencode(postTabledict).encode("UTF-8")

    return post_data
postData = postKeyGather()                                          # call once

# ======================get format time, and get year-month-date to be a folder name===============================

# real time clock
rtc = time.localtime()
ymd = '%d-%d-%d' % (rtc[0], rtc[1], rtc[2])

def OSFileManager():
    """
        define os gui file manager
        :return:    file manager name
    """
    fm = ''
    if os.name == 'posix':
        fm = 'nautilus'
    elif os.name == 'nt':
        fm = 'explorer'
    return fm

def SetOSHomeFolder ():
    """
        set os platform to set folder format
        :return:    platform work directory
    """
    homeFolder = ''
    # linux
    if os.name == 'posix':
        homeFolder = '/home/neod-anderjon/Pictures/Crawler/'
    # windows
    elif os.name == 'nt':
        homeFolder = 'E:\\Workstation_Files\\Pictures\\Comic\\IllustratorDesign\\Crawler\\'

    return homeFolder
workDir = SetOSHomeFolder()                                         # call once

# universal path
logFileName = '/CrawlerWork[%s].log' % ymd
htmlFileName = '/CrawlerWork[%s].html' % ymd
privateFolder = workDir + 'RankTop_%s' % ymd
# daily-rank path
logFilePath = privateFolder + logFileName
htmlFilePath = privateFolder + htmlFileName

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
