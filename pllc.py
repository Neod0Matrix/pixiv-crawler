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

import time, os, linecache                                          # name folder and files

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
    if os.name == 'posix':
        loginDataHeader = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
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
    elif os.name == 'nt':
        loginDataHeader = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br",
            'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
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

# login mainpage
def SetUserAgentForMainPage(referer):
    # linux
    if os.name == 'posix':
        DataHeader = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "br",
            'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            'DNT': "1",
            'Host': "www.pixiv.net",
            'Upgrade-Insecure-Requests': "1",
            'Referer': referer,
            'User-Agent': useragentForLinuxBrowser,
        }
    # windows
    elif os.name == 'nt':
        DataHeader = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "br",
            'Accept-Language': "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4,zh-CN;q=0.2",
            'Cache-Control': "max-age=0",
            'Connection': "keep-alive",
            'DNT': "1",
            'Host': "www.pixiv.net",
            'Upgrade-Insecure-Requests': "1",
            'Referer': referer,
            'User-Agent': useragentForWindowsBrowser,
        }

    return DataHeader

# login.cr read or manual input
loginCrFile = 'login.cr'                                            # login info file
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

loginInfo = LoginInfoLoad()

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
# GET way need info
getwayRegInfo = [('user', loginInfo[0]), ('pass', loginInfo[1])]

# ========================================some use url address=====================================================
# maybe pixiv use https proxy, but here must write http proxy, or not you will have httplib.BadStatusLine: '' error
hostWebURL = 'http://www.pixiv.net/'
rankWebURL = 'http://www.pixiv.net/ranking.php?mode=daily&content=illust' # dailyRank
rankWebURL_R18 = 'https://www.pixiv.net/ranking.php?mode=daily_r18&content=illust&ref=rn-h-r18-3'
baseWebURL = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' # basic format
illustHomeURL = 'http://www.pixiv.net/member.php?id='               # illust home page

# illust mainpage artwork index
def illustArtworkIndex(setid):
    return 'http://www.pixiv.net/member_illust.php?id=' + setid + '&type=all'

# =======================================regex collection==========================================================
rankURLRegex = '<section.*?data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)" data-date="(.*?)".*?data-id="(.*?)"'
imgThumbnailRegex = '<img src=".*?"'                                # many strings array
nbrRegex = '\d+\.?\d*'                                              # cut number

# illust artwork count mate
def illustAWCntRegex(setid):
    return 'eRegister" data-user-id="%s">.*?<' % setid

def illustAWIndexRegex(setid):
    return 'illust_id=' + setid + '"class'

# ======================get format time, and get year-month-date to be a folder name===============================
ymdRealTime = time.localtime()
image_header = '%s-%s-%s-' % (str(ymdRealTime[0]), str(ymdRealTime[1]), str(ymdRealTime[2]))

fileManager = 'nautilus'                                            # define os gui file manager

# set os platform to set folder format
def SetOSHomeFolder ():
    # linux
    if os.name == 'posix':
        homeFolder = '/home/neod-anderjon/LTEProjects/pixiv_collection/'
    # windows
    elif os.name == 'nt':
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
