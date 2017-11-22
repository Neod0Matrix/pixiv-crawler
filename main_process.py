#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to run main process

import pllc, daily_rank, illust_repo

pllc.EncodeDecodeResolve()

if __name__ == '__main__':
    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')
    if mode == 'drt':
        print pllc.SHELLHEAD + "check mode: dailyRankTop"
        daily_rank.DailyRankTop().drtStartCrawler()
    elif mode == 'ira':
        print pllc.SHELLHEAD + "check mode: illustRepoAll"
        illust_repo.IllustRepoAll().iraStartCrawler()
    elif mode == 'help':
        print pllc.SHELLHEAD +                                                                  \
              "code by </MATRIX>@Neod Anderjon(LeaderN)\n"                                      \
              "MatPixivCrawler Help Page\n"                                                     \
              "drt  ---     dailyRankTop, crawl Pixiv daily-rank top N(N<=50) artwork(s)\n"     \
              "ira  ---     illustRepoAll, crawl Pixiv any illustrator 20(max) artwork(s)\n"    \
              "help ---     print this help page\n"
    else:
        print pllc.SHELLHEAD + "argv(s) error\n"

# =====================================================================
# code by </MATRIX>@Neod Anderjon
