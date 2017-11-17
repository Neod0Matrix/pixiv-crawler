#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# this test script is written to log pixiv login data in linux chrome env
# pllc is pixiv login linux chrome
# code by </MATRIX>@Neod Anderjon
# =====================================================================

# projrct info
__author__          = 'Neod Anderjon'                               # author signature
__laboratory__      = 'T.WKVER'                                     # lab
__organization__    = '</MATRIX>'
__version__         = 'v0p8_LTE'                                    # version string

import time, os                                                     # name folder and files

SHELLHEAD = 'MatPixivCrawler@' + __organization__ + ':~$ '          # copy linux head symbol

# ==============================================pixiv login data====================================================
reqSuccessCode = 200
# user-agent, chrome version ignore
useragentForLinuxBrowser = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                           "Chrome/56.0.2924.87 Safari/537.36"
useragentForWindowsBrowser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                             " Chrome/60.0.3112.90 Safari/537.36"

# headers data use in http request
def SetUserAgentHeader():
    # linux
    if os_name == 'posix':
        loginDataHeader = {
            ## 'Accept': "application/json, text/javascript, */*; q=0.01",
            ## 'Accept-Encoding': "gzip, deflate, br",
            ## 'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
            'Connection': "keep-alive",
            'Content-Length': reqSuccessCode,
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "accounts.pixiv.net",
            'Origin': "http://accounts.pixiv.net",
            ## 'Upgrade-Insecure-Requests': "1",
            'Referer': "http://www.pixiv.net/login.php?return_to=0",
            'User-Agent': useragentForLinuxBrowser,
            'X-Requested-With': "XMLHttpRequest",
        }
    # windows
    elif os_name == 'nt':
        loginDataHeader = {
            ## 'Accept': "application/json, text/javascript, */*; q=0.01",
            ## 'Accept-Encoding': "gzip, deflate, br",
            ## 'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
            'Connection': "keep-alive",
            'Content-Length': reqSuccessCode,
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Host': "accounts.pixiv.net",
            'Origin': "http://accounts.pixiv.net",
            ## 'Upgrade-Insecure-Requests': "1",
            'Referer': "http://www.pixiv.net/login.php?return_to=0",
            'User-Agent': useragentForWindowsBrowser,
            'X-Requested-With': "XMLHttpRequest",
        }

    return loginDataHeader

# login account
userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(e-mailbox), must can be a R18: ')
userPassword = raw_input(SHELLHEAD + 'enter your id password: ')
# POST way to login
postwayRegInfo = {
            'mode': 'login', # this mode login my chrome browser has no
            'pixiv_id': userMailBox,
            'pass': userPassword,
            ## 'captcha': "",
            ## 'g_recaptcha_response': "",
            ## 'source': "pc",
            ## 'ref': "wwwtop_accounts_index",
            'return_to': 'http://www.pixiv.net/',
            'skip': 1 # this skip parameter my chrome has no
        }
# GET way need info
getwayRegInfo = [('user', userMailBox), ('pass', userPassword)]

# ========================================some use url address=====================================================
# maybe pixiv use https proxy, but here must write http proxy, or not you will have httplib.BadStatusLine: '' error
hostWebURL = 'http://www.pixiv.net/'
rankWebURL = 'http://www.pixiv.net/ranking.php?mode=daily&content=illust' # dailyRank
baseWebURL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' # basic format
illustHomeURL = 'http://www.pixiv.net/member.php?id='               # illust home page
illustArtworkIndex = 'http://www.pixiv.net/member_illust.php?id='   # artwork index

# =====================================regex for dailyRank and image================================================
rankURLRegex = '<section.*?data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)" data-date="(.*?)".*?data-id="(.*?)"'
imgThumbnailRegex = '<img src=".*?"'                                # many strings array

# illust artwork count mate
def illustAWCntRegex(setid):
    return 'eRegister" data-user-id="%s">.*?<' % setid

# ======================get format time, and get year-month-date to be a folder name===============================
ymdRealTime = time.localtime()
image_header = '%s-%s-%s-' % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))

fileManager = 'nautilus'                                            # define os gui file manager
os_name = os.name                                                   # get os platform type

# set os platform to set folder format
def SetOSHomeFolder ():
    # linux
    if os_name == 'posix':
        homeFolder = '/home/neod-anderjon/LTEProjects/pixiv_collection/'
    # windows
    elif os_name == 'nt':
        homeFolder = 'E:/pixiv_collection/'

    return homeFolder

privateFolder = SetOSHomeFolder() + '%s-%s-%s' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))
# crawler work log
logFilePath = privateFolder + '/PixivCrawlerLog-%s-%s-%s.log' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))
# illuster info
illustInfoFilePath = privateFolder + '/PixivCrawlerTopInfo-%s-%s-%s.info' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))
# time log
excFinishTime = '%s-%s-%s %s:%s:%s' \
            % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]), str(ymdRealTime[3]), str(ymdRealTime[4]), str(ymdRealTime[5]))

# =====================================================================
# code by </MATRIX>@Neod Anderjon
