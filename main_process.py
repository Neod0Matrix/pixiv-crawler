#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to run main process

import pllc, priv_lib, daily_rank, illust_repo

pp = priv_lib.PrivateLib()
pllc.EncodeDecodeResolve()
helpPage = pp.__doc__

if __name__ == '__main__':
    print helpPage
    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')
    if mode == 'drt' or mode == '1':
        print pllc.SHELLHEAD + "check mode: dailyRankTop"
        daily_rank.DailyRankTop().drtStartCrawler()
    elif mode == 'ira' or mode == '2':
        print pllc.SHELLHEAD + "check mode: illustRepoAll"
        illust_repo.IllustRepoAll().iraStartCrawler()
    elif mode == 'help':
        print helpPage
    else:
        print pllc.SHELLHEAD + "argv(s) error\n"
        exit()

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
