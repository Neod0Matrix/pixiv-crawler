#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon
# =====================================================================
# this python script is built to call fuction or class

import pllc, daily_rank, illust_repo

# main fuction
def crawlerCallHandler ():
    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')
    if mode == 'drt':
        print pllc.SHELLHEAD + "dailyRankTop mode"
        daily_rank.DailyRankTop().drtStartCrawler()
    elif mode == 'ira':
        print pllc.SHELLHEAD + "illustRepoAll mode"
        illust_repo.IllustRepoAll().iraStartCrawler()
    elif mode == 'h':
        print pllc.SHELLHEAD + \
              "code by </MATRIX>@Neod Anderjon\n" \
              "MatPixivCrawler Help Page\n" \
              "drt  ---     dailyRankTop mode\n" \
              "ira  ---     illustRepoAll mode\n" \
              "h    ---     help page\n"
    else:
        print pllc.SHELLHEAD + "argv error\n"

    return mode

if __name__ == '__main__':
    crawlerCallHandler()

# =====================================================================
# code by </MATRIX>@Neod Anderjon
