License
======
    
    Copyright @2017 T.WKVER </MATRIX>
    Code by </MATRIX>@Neod Anderjon(LeaderN)
    Thanks to fork and watch my project

Update
======

    Version: v3p0_LTE 
    Last Update Time: 20171122pm1404
    
    This python crawler is built to crawl pixiv images
    It have two mode: dailyRankTop and illustRepoAll 
    * This version's illustRepoAll mode haven't been finished, it can only get less than 20 images
    Please run in a good network, in some contry and area, it may crawl slowly

Platform
======

    Linux x86_64 kernel or Windows NT
    Python: 2.7+
    Python crawler regular-module depend: urllib, urllib2, cookielib, re, json
    others are essential module, python will auto-install
    You need to use browser's javascript console to check your system user-agent
    All needed data in pllc.py, please check all then run pixiv-crawler.py

Run
======

    * git clone https://github.com/Neod0Matrix/pixiv-crawler.git
    First config your local folder in pllc.py and login.cr

Linux / Windows
> $ python main_process.py

Problems that may arise
======

    May the good network with you

    If you frequently use the crawler to request resources from the server, 
    then after some time the server may throw you 10060 error, 
    just wait for a second and ok
    
    If your test network environment has been dns-polluted, I suggest you 
    fix your PC dns-server to a pure server
    In China, such as 115.159.146.99 from https://aixyz.com/
    
    ira mode you need input that illuster id ,not image id
    crawler log image will rename to array number + image id, 
    you can use this id to find original image in Pixiv website
    
    Pixiv website will often change the image URL, please use the lastest results from javascript console
    
    Because Pixiv set an author of all the artworks into each page shows up to 20 images, 
    so that if crawler crawls more than 20 images, it must request different URL pages several times, 
    which is ... damn it!
    I try to request others page, but server give the same page...hehe
    
    Remember delete login.cr info before push or commit issue
    
    About pixiv dailyRank R18, I try to build new headers to request, but server give me a 403 error, 
    I can't understand it
    
    If you can resolve the two question: mainpage request only first page and daily-rank r18 403 error,
    you will crawl all of Pixiv website artworks with this crawler
