License
======
    
    Copyright @2017 T.WKVER </MATRIX>
    Code by </MATRIX>@Neod Anderjon(LeaderN)
    Thanks to fork and watch my project

Update
======

    Version: v2p1_LTE 
    Last Update Time: 20171120am0125
    
    This python crawler is built to crawl pixiv images
    It have two mode: dailyRankTop and illustRepoAll 
    * This version's illustRepoAll mode haven't been finished, it can only get less than 20 images
    Please run in a good network, in some contry and area, it may crawl slowly

Platform
======

    Linux x86_64 kernel or Windows NT
    Python: 2.7+
    Python-module need: urllib, urllib2, cookielib, re, os, json
    You need to use browser's javascript console to check your system user-agent
    All needed data in pllc.py, please check all then run pixiv-crawler.py

Run
======

    * git clone https://github.com/Neod0Matrix/pixiv-crawler.git
    First config your local folder in pllc.py
    Then:
    Linux / Windows
    $ python pixiv-crawler.py

Problems that may arise
======

    If you frequently use the crawler to request resources from the server, 
    then after some time the server may throw you 10060 error, 
    just wait for a second and ok
    
    Pixiv website will often change the image URL, please use the lastest results from javascript console
    
    Because Pixiv set an author of all the artworks into each page shows up to 20 images, 
    so that if crawler crawls more than 20 images, it must request different URL pages several times, 
    which is ... damn it!
    So this version can only be done here, thank you for your support and fork
