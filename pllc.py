#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this test script is written to handle datas and some info

# projrct info
__author__          = 'Neod Anderjon(LeaderN)'                      # author signature
__laboratory__      = 'T.WKVER'                                     # lab
__organization__    = '</MATRIX>'
__version__         = 'v3p7_LTE'

import urllib2, re, urllib, json                                    # post data build
import time, os, linecache, sys                                     # name folder and files
import getpass                                                      # user and passwd input

SHELLHEAD = 'MatPixivCrawler@' + __organization__ + ':~$ '          # copy linux head symbol

# ==============================================pixiv login info====================================================

# resolve encode/decode question
def EncodeDecodeResolve():
    reload(sys)
    sys.setdefaultencoding('UTF-8')

EncodeDecodeResolve()                                               # run once just ok

# login user info file, must be ran firstly
loginCrFile = 'login.cr'
# .cr file example:
# =================================
# [login]
# <mail>
# <passwd>
# =================================
def LoginInfoLoad():
    print '###########################[pixiv-crawler(MatPixivCrawler) %s]###########################' % __version__

    loginFilePath = os.getcwd() + '/' + loginCrFile                 # get local dir path
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
            print SHELLHEAD + "please check your info:\n" + userMailBox + userPassword # no log in log file
            check = raw_input(SHELLHEAD + "Yes or No?: ")
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

    return userMailBox, userPassword

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
# request universal original image constant words
imgOriginalheader = 'https://i.pximg.net/img-original/img'          # original image https url header
imgOriginaltail = '_p0.png'                                         # original image https url tail, default set to png
# page request http proxy
rankWebURL = 'http://www.pixiv.net/ranking.php?mode=daily'          # dailyRank
rankWebURL_R18 = 'http://www.pixiv.net/ranking.php?mode=daily_r18'  # r18 dailyRank
baseWebURL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' # basic format
illustHomeURL = 'http://www.pixiv.net/member.php?id='               # illust home page
mainPage = 'http://www.pixiv.net/member_illust.php?id='             # illust main page
mainPagemiddle = '&type=all'                                        # url middle word
mainPagetail = '&p='                                                # url tail word

# ==================================http request headers include data============================================

reqSuccessCode = 200
# login headers info dict
useragentForLinuxBrowser = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                           "Chrome/56.0.2924.87 Safari/537.36"
useragentForWindowsBrowser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                            " Chrome/60.0.3112.90 Safari/537.36"
accept = "application/json, text/javascript, */*; q=0.01"
accept2 = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
acceptEncoding = "gzip, deflate, br"
acceptEncoding2 = "br"                                              # no use gzip, transfer speed down, but will not error
acceptLanguage = "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2"
connection = "keep-alive"
contentType = "application/x-www-form-urlencoded; charset=UTF-8"
xRequestwith = "XMLHttpRequest"

# init
def InitLoginHeaders():
    baseHeaders = {
        'Accept': accept,
        'Accept-Encoding': acceptEncoding,
        'Accept-Language': acceptLanguage,
        'Connection': connection,
        'Content-Length': "207",
        'Content-Type': contentType,
        'DNT': "1",
        'Host': accountHost,
        'Origin': originHost,
        'Referer': postKeyGeturl,                                   # last page is request post-key page
        'X-Requested-With': xRequestwith,
    }
    buildHeaders = {}
    # linux
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': useragentForLinuxBrowser,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': useragentForWindowsBrowser,
        }.items())

    return buildHeaders

# r18 daily-rank
def R18DailyRankRequestHeaders():
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
            'User-Agent': useragentForLinuxBrowser,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': useragentForWindowsBrowser,
        }.items())

    return buildHeaders

# mainpage
def MainpageRequestHeaders(referer):
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
            'User-Agent': useragentForLinuxBrowser,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': useragentForWindowsBrowser,
        }.items())

    return buildHeaders

# original image
def OriginalImageRequestHeaders(referer):
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
            'User-Agent': useragentForLinuxBrowser,
        }.items())
    # windows
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': useragentForWindowsBrowser,
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
# illust artwork count mate
def illustAWCntRegex(setid):
    return 'eRegister" data-user-id="%s">.*?<' % setid
# ======================================login need word build================================================
# http request have more way, Pixiv use POST way to login and request image, use GET way to request page

# GET way need info
getwayRegInfo = [('user', loginInfo[0]), ('pass', loginInfo[1])]    # priv_lib will first init it
getData = json.dumps(urllib.urlencode(getwayRegInfo))               # call once

# POST way build dict
def postKeyGather():
    # build basic dict
    postwayRegInfo = {
            'pixiv_id': loginInfo[0],
            'password': loginInfo[1],
            'captcha': "",
            'g_recaptcha_response': "",
            'source': "pc",
            'ref': login_ref,
            'return_to': hostWebURL,
        }
    request = urllib2.Request(postKeyGeturl)
    response = urllib2.urlopen(request, timeout=300)
    # mate post key
    web_src = response.read().decode("UTF-8", "ignore")
    postPattern = re.compile(postKeyRegex, re.S)
    postKey = re.findall(postPattern, web_src)[0]
    print SHELLHEAD + 'get post-key: ' + postKey                    # display key
    # build total post data
    postKeydict = {'post_key': postKey}
    post_dict = dict(postwayRegInfo.items() + postKeydict.items())
    post_data = json.dumps(urllib.urlencode(post_dict))

    return post_data

postData = postKeyGather()                                          # call once

# ======================get format time, and get year-month-date to be a folder name===============================

# real time clock
rtc = time.localtime()
ymd = '%d-%d-%d' % (rtc[0], rtc[1], rtc[2])

# define os gui file manager
def OSFileManager():
    fm = ''
    if os.name == 'posix':
        fm = 'nautilus'
    elif os.name == 'nt':
        fm = 'explorer'
    return fm

# set os platform to set folder format
def SetOSHomeFolder ():
    homeFolder = ''
    # linux
    if os.name == 'posix':
        homeFolder = '/home/neod-anderjon/Pictures/Crawler/'
    # windows
    elif os.name == 'nt':
        homeFolder = 'E:\\Workstation_Files\\Pictures\\Comic\\IllustratorDesign\\Crawler\\'

    return homeFolder

workDir = SetOSHomeFolder()                                         # call once

# private directory
privateFolder = workDir + 'DailyRank_%s' % ymd                      # daily-rank use
logFileName = '/CrawlerWork[%s].log' % ymd                          # universal name
logFilePath = privateFolder + logFileName                           # daily-rank use

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
