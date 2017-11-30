#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this test script is written to handle datas and some info

# projrct info
__author__          = 'Neod Anderjon(LeaderN)'                      # author signature
__laboratory__      = 'T.WKVER'                                     # lab
__organization__    = '</MATRIX>'
__version__         = 'v5p2_LTE'

import urllib, json
import time, os, linecache, sys
import getpass

SHELLHEAD = 'MatPixivCrawler@' + __organization__ + ':~$ '          # copy linux head symbol

# ==============================================pixiv login info====================================================

def encode_resolve():
    """
        use reload sys to resolve python damn encode question
        :return:    none
    """
    reload(sys)
    sys.setdefaultencoding('UTF-8')
encode_resolve()                                                    # run once just ok

def login_infopreload():
    """
        get user input username and password
        login.cr file example:
        =================================
        [login]
        <mail>
        <passwd>
        =================================
        :return:    username, password, get data
    """
    print "###################################login data check###################################"
    loginFilePath = os.getcwd() + '/' + 'login.cr'                  # get local dir path
    isLoginCrExisted = os.path.exists(loginFilePath)
    if isLoginCrExisted:
        userMailBox = linecache.getline(loginFilePath, 2)           # row 2, usernamemail
        userPassword = linecache.getline(loginFilePath, 3)          # row 3, password
        # empty file
        if userMailBox == '' or userPassword == '':
            print SHELLHEAD + "login.cr file invaild, please input your login info"
            userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
            userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ') # pycharm python console not support
        else:
            check = raw_input(SHELLHEAD + "please check your info:\n"
                                          "[!]    username: %s[!]    password: %s"
                                          "Yes or No?: " % (userMailBox, userPassword))
            # user judge info are error
            if check != 'yes' and check != 'Yes' and check != 'YES' and check != 'y' and check != 'Y':
                print SHELLHEAD + "you can write new info"
                userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
                userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ')
            else:
                pass
    # no login.cr file
    else:
        print SHELLHEAD + "cannot find login.cr file, please input your login info"
        userMailBox = raw_input(SHELLHEAD + 'enter your pixiv id(mailbox), must be a R18: ')
        userPassword = getpass.getpass(SHELLHEAD + 'enter your account password: ')

    # strip() delete symbol '\n'
    username = userMailBox.strip()
    passwd = userPassword.strip()

    getwayRegInfo = [('user', username), ('pass', passwd)]
    getData = json.dumps(urllib.urlencode(getwayRegInfo))           # transfer format

    return username, passwd, getData
login_data = login_infopreload()                                    # preduce call once

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

def dict_transto_list (input_dict):
    """
        change dict data-type to list
        :param input_dict:      dict
        :return:                list
    """
    result_list = []
    for key, value in input_dict.items():
        item = (key, value)
        result_list.append(item)

    return result_list

def build_login_headers(cookie):
    """
        build the first request login headers
        :param cookie:  cookie
        :return:        login headers
    """
    # this build headers key-word is referer and user-agent
    baseHeaders = {
        'Accept': accept,
        'Accept-Encoding': acceptEncoding,
        'Accept-Language': acceptLanguage,
        'Cache-Control': cacheControl,
        'Connection': connection,
        'Content-Length': "207",
        'Content-Type': contentType,
        'Cookie': cookie,
        'DNT': "1",
        'Host': accountHost,
        'Origin': originHost2,
        'Referer': postKeyGeturl,                                   # last page is request post-key page
        'X-Requested-With': xRequestwith,
    }
    buildHeaders = {}
    # platform choose
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())
    else:
        pass

    return buildHeaders

def build_original_headers(referer):
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
    # platform choose
    if os.name == 'posix':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentLinux,
        }.items())
    elif os.name == 'nt':
        buildHeaders = dict(baseHeaders.items() + {
            'User-Agent': userAgentWindows,
        }.items())
    else:
        pass

    return buildHeaders

# =======================================regex collection==========================================================

postKeyRegex = 'key".*?"(.*?)"'                                     # mate post key
rankTitleRegex = '<section.*?data-rank-text="(.*?)" data-title="(.*?)" data-user-name="(.*?)" data-date="(.*?)".*?data-id="(.*?)"'
rankVWRegex = 'r/img/.*?_'                                          # from dailyRank page gather vaild words
nbrRegex = '\d+\.?\d*'                                              # mate any number
imgThumbnailRegex = '<img src="(.*?)"'                              # mate thumbnail image
mainpageThumbnailRegex = '-src=".*?"'                               # mainpage use thumbnail regex
illustNameRegex = 'me"title=".*?"'                                  # mate illust name
imagesNameRegex = 'e" title=".*?"'                                  # mate mainpage images name
proxyServerRegex = 'tr'                                             # use beautifulsoup module, easy
arrangeProxyServerRegex = 'td'                                      # cut gather list
illustAWCntRegex = 'dge">.*?<'                                      # illust artwork count mate

# ======================get format time, and get year-month-date to be a folder name===============================

def platform_filemanager():
    """
        define os gui file manager
        :return:    file manager name
    """
    fm = ''
    if os.name == 'posix':
        fm = 'nautilus'
    elif os.name == 'nt':
        fm = 'explorer'
    else:
        pass
    return fm

def setting_platform_workdir ():
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
    else:
        pass

    return homeFolder
work_dir = setting_platform_workdir()                               # call once

# real time clock
rtc = time.localtime()
ymd = '%d-%d-%d' % (rtc[0], rtc[1], rtc[2])

# universal path
logfile_name = '/CrawlerWork[%s].log' % ymd
htmlfile_name = '/CrawlerWork[%s].html' % ymd
ranking_folder = work_dir + 'RankTop_%s' % ymd                      # two layer folder
# daily-rank path
logfile_path = ranking_folder + logfile_name
htmlfile_path = ranking_folder + htmlfile_name

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
