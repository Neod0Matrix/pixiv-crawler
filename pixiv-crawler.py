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
        daily_rank.DailyRankTop().drtStartCrawler()
    elif mode == 'ira':
        # illust_repo.IllustRepoAll().StartCrawlerWork()
        print pllc.SHELLHEAD + "this fuction haven't built\n"
    else:
        print pllc.SHELLHEAD + "argv error\n"

if __name__ == '__main__':
    crawlerCallHandler()

# =====================================================================
# code by </MATRIX>@Neod Anderjon
