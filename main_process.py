#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to run main process

import pllc, priv_lib, rank_top, illust_repo

pllc.EncodeDecodeResolve()

if __name__ == '__main__':
    pp = priv_lib.PrivateLib()
    print pp.__doc__
    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')
    if mode == 'rtn' or mode == '1':
        print pllc.SHELLHEAD + "check mode: RankTopN"
        rank_top.RankingTopN().rtnStartCrawler()
    elif mode == 'ira' or mode == '2':
        print pllc.SHELLHEAD + "check mode: illustRepoAll"
        illust_repo.IllustRepoAll().iraStartCrawler()
    elif mode == 'help':
        print pp.__doc__
    else:
        mode = None
        print pllc.SHELLHEAD + "argv(s) error\n"
        print pp.__doc__

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
