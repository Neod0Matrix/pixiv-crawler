#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this test script is written to handle datas and some info

# projrct info
__author__          = 'Neod Anderjon'                               # author signature
__laboratory__      = 'T.WKVER'                                     # lab
__organization__    = '</MATRIX>'
__version__         = 'v2p9_LTE'                                    # version string

import time, os, linecache, sys                                     # name folder and files

SHELLHEAD = 'MatPixivCrawler@' + __organization__ + ':~$ '          # copy linux head symbol

# ==============================================pixiv login info====================================================

# resolve encode/decode question for gbk encode webpage
def EncodeDecodeResolve():
    reload(sys)
    sys.setdefaultencoding('UTF-8')

EncodeDecodeResolve()                                               # run once just ok

reqSuccessCode = 200
# login headers info dict
useragentForLinuxBrowser = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                           "Chrome/56.0.2924.87 Safari/537.36"
useragentForWindowsBrowser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                            " Chrome/60.0.3112.90 Safari/537.36"
accept = "application/json, text/javascript, */*; q=0.01"
acceptEncoding = "gzip, deflate, br"
acceptEncoding2 = "br"
acceptLanguage = "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2"
connection = "keep-alive"
contentType = "application/x-www-form-urlencoded; charset=UTF-8"
xRequestwith = "XMLHttpRequest"

accountHost = "accounts.pixiv.net"
originHost = "http://accounts.pixiv.net"
loginReferer = "http://www.pixiv.net/login.php?return_to=0"
wwwHost = "www.pixiv.net"

# login user info file
loginCrFile = 'login.cr'

# ========================================some use url address=====================================================
# maybe pixiv use https proxy, but here must write http proxy, or not you will have httplib.BadStatusLine: '' error
hostWebURL = 'http://www.pixiv.net/'
rankWebURL = 'http://www.pixiv.net/ranking.php?mode=daily&content=illust' # dailyRank
rankWebURL_R18 = 'http://www.pixiv.net/ranking.php?mode=daily_r18&content=illust' # r18 dailyRank
baseWebURL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' # basic format
illustHomeURL = 'http://www.pixiv.net/member.php?id='               # illust home page
mainPage = 'http://www.pixiv.net/member_illust.php?id='             # illust main page
mainPagemiddle = '&type=all'                                        # url middle word
mainPagetail = '&p='                                                # url tail word
# request universal original image constant words
imgOriginalheader = 'https://i.pximg.net/img-original/img'          # original image https url header
imgOriginaltail = '_p0.png'                                         # original image https url tail, default set to png

# =======================================regex collection==========================================================

rankTitleRegex = '<section.*?data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)" data-date="(.*?)".*?data-id="(.*?)"'
rankVWRegex = 'r/img/.*?_'                                          # from dailyRank page gather vaild words
nbrRegex = '\d+\.?\d*'                                              # mate any number
imgThumbnailRegex = '<img src="(.*?)"'                              # mate thumbnail image
illustNameRegex = 'r:title" content=".*? '                          # mate illust name
imagesNameRegex = '" alt="(.*?)"'                                   # mate images name
# illust artwork count mate
def illustAWCntRegex(setid):
    return 'eRegister" data-user-id="%s">.*?<' % setid

# ======================get format time, and get year-month-date to be a folder name===============================

ymdRealTime = time.localtime()
image_header = '%s-%s-%s-' % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))

fileManager = 'nautilus'                                            # define linux gui file manager

# set os platform to set folder format
def SetOSHomeFolder ():
    homeFolder = ''
    # linux
    if os.name == 'posix':
        homeFolder = '/home/neod-anderjon/LTEProjects/pixiv_collection/'
    # windows
    elif os.name == 'nt':
        homeFolder = 'E:/pixiv_collection/'

    return homeFolder

workDir = SetOSHomeFolder()

privateFolder = workDir + '%s-%s-%s' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))

logFileName = '/CrawlerWork[%s-%s-%s].log' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))
# crawler work log
logFilePath = privateFolder + logFileName
# time log
excFinishTime = '%s-%s-%s %s:%s:%s' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]), str(ymdRealTime[3]), str(ymdRealTime[4]), str(ymdRealTime[5]))

# =================================build request use headers fuction=========================================

# init
def InitLoginHeaders():
    baseHeaders = {
        'Accept': accept,
        'Accept-Encoding': acceptEncoding,
        'Accept-Language': acceptLanguage,
        'Connection': connection,
        'Content-Length': reqSuccessCode,
        'Content-Type': contentType,
        'Host': accountHost,
        'Origin': originHost,
        ## 'Upgrade-Insecure-Requests': "1",
        'Referer': loginReferer,
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

# mainpage
def MainpageRequestHeaders(referer):
    baseHeaders = {
        'Accept': accept,
        'Accept-Encoding': acceptEncoding2,
        'Accept-Language': acceptLanguage,
        'Cache-Control': "max-age=0",
        'Connection': connection,
        'DNT': "1",
        'Host': wwwHost,
        'Upgrade-Insecure-Requests': "1",
        'Referer': referer,
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

# =================================
# [login]
# <mail>
# <passwd>
# =================================
def LoginInfoLoad():
    loginFilePath = os.getcwd() + '/' + loginCrFile                 # get local dir path
    isLoginCrExisted = os.path.exists(loginFilePath)
    if isLoginCrExisted:
        userMailBox = linecache.getline(loginFilePath, 2)           # row 2, usernamemail
        userPassword = linecache.getline(loginFilePath, 3)          # row 3, password
        # empty file
        if userMailBox == '' or userPassword == '':
            print SHELLHEAD + "login.cr file invaild, please input your login info"
            userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(e-mailbox), must can be a R18: ')
            userPassword = raw_input(SHELLHEAD + 'enter your id password: ')
        else:
            print SHELLHEAD + "please check your info:\n" + userMailBox + userPassword
            check = raw_input(SHELLHEAD + "Yes or No?: ")
            # check error
            if check != 'yes' and check != 'Yes' and check != 'YES' and check != 'y' and check != 'Y':
                print SHELLHEAD + "you can write new info"
                userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(e-mailbox), must can be a R18: ')
                userPassword = raw_input(SHELLHEAD + 'enter your id password: ')
    # no login.cr file
    else:
        print SHELLHEAD + "cannot find login.cr file, please input your login info"
        userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(e-mailbox), must can be a R18: ')
        userPassword = raw_input(SHELLHEAD + 'enter your id password: ')

    return userMailBox, userPassword

# GET way need info
loginInfo = LoginInfoLoad()
getwayRegInfo = [('user', loginInfo[0]), ('pass', loginInfo[1])]
# POST way to login
postwayRegInfo = {
            'mode': 'login', # this mode login my chrome browser has no
            'pixiv_id': loginInfo[0],
            'pass': loginInfo[1],
            ## 'captcha': "",
            ## 'g_recaptcha_response': "",
            ## 'source': "pc",
            ## 'ref': "wwwtop_accounts_index",
            'return_to': 'http://www.pixiv.net/',
            'skip': 1 # this skip parameter my chrome has no
        }

# =====================================================================
# code by </MATRIX>@Neod Anderjon
