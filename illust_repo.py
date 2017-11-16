#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to get a illust all repo images

import urllib, urllib2, cookielib, re, os, json                     # crawler depends
import pllc                                                         # messages

# create a class for pixiv dailyRank top
class IllustRepoAll:
    # class include init process
    def __init__(self):
        # request sheet
        self.loginURL = pllc.hostWebURL                             # pixiv login page
        # javascript console's headers dict
        # only use in linux's google chrome
        self.loginHeader = pllc.loginDataHeader
        # use post way to request service
        self.postData = json.dumps(urllib.urlencode(pllc.postwayRegInfo))
        # get local cookie, create a opener for pixiv class
        self.cookie = cookielib.LWPCookieJar()                      # use last sheet to create a cookie-module
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.cookieHandler)

# =====================================================================
# code by </MATRIX>@Neod Anderjon
