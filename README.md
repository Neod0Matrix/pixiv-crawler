[![Python 2.7](https://img.shields.io/badge/Python-2.7-yellow.svg)](http://www.python.org/download/)

# pixiv-crawler - Pixiv images and messages crawler

    ██████╗ ██╗██╗  ██╗██╗██╗   ██╗       ██████╗██████╗  █████╗ ██╗    ██╗██╗     ███████╗██████╗ 
    ██╔══██╗██║╚██╗██╔╝██║██║   ██║      ██╔════╝██╔══██╗██╔══██╗██║    ██║██║     ██╔════╝██╔══██╗
    ██████╔╝██║ ╚███╔╝ ██║██║   ██║█████╗██║     ██████╔╝███████║██║ █╗ ██║██║     █████╗  ██████╔╝
    ██╔═══╝ ██║ ██╔██╗ ██║╚██╗ ██╔╝╚════╝██║     ██╔══██╗██╔══██║██║███╗██║██║     ██╔══╝  ██╔══██╗
    ██║     ██║██╔╝ ██╗██║ ╚████╔╝       ╚██████╗██║  ██║██║  ██║╚███╔███╔╝███████╗███████╗██║  ██║
    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝         ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝

ascii artword from http://patorjk.com/software/taag/

License
======
    
    Copyright (c) 2017 @T.WKVER </MATRIX>
    Code by </MATRIX>@Neod Anderjon(LeaderN)
    MIT license read in LICENSE
    Thanks to fork and watch my project

Update
======

    Version: v5p1_LTE 
    Last Update Time: 20171130am0032
    
    This python crawler is built to crawl pixiv images
    It have two mode: RankTopN and illustRepoAll 
    Call threading to add multi-process download images
    Two mode for requesting original images

Platform
======

    Linux x86_64 kernel and Windows NT
    Python: 2.7+(2.6 may be too old, and not support 3.x)

## Requirements

* urllib
* urllib2
* beautifulsoup4
* json
* getpass
* cookielib
* threading
* PIL

Run
======

- [pixiv-crawler](https://github.com/Neod0Matrix/pixiv-crawler)
    git clone https://github.com/Neod0Matrix/pixiv-crawler.git
    
    cd pixiv-crawler
    
    First config your local folder in pllc.py and login.cr
    
    python main_process.py

Problems that may arise
======

    May the good network status with you

    If you use the crawler too often to request data from the server, 
    the server may return an 10060 error for you, 
    just need to wait for a while and then try again, or use a proxy server
    
    If your test network environment has been dns-polluted, I suggest you 
    fix your PC dns-server to a pure server
    In China, such as 115.159.146.99 from https://aixyz.com/
    
    ira mode you need input that illuster id ,not image id
    crawler log image will rename to array number + image id, 
    you can use this id to find original image with URL:
    https://www.pixiv.net/member_illust.php?mode=medium&illust_id=<your known id>
    
    Pixiv website will often change the image URL frame, 
    please use the lastest results from javascript console
    
    Remember delete login.cr info before push or commit issue
    
    Login successed, Pixiv sees the post-data rather than the headers,
    as long as the opener is guaranteed to be used correctly, 
    no headers can be successfully logged in
    Now you can use this crawler to crawl all target from Pixiv
    