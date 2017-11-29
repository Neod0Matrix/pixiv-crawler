#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to run main process

import pllc, priv_lib, rank_top, illust_repo

pllc.encode_resolve()

if __name__ == '__main__':
    pp = priv_lib.PrivateLib()
    print pp.__doc__

    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')
    if mode == 'rtn' or mode == '1':
        print pllc.SHELLHEAD + "check mode: RankTopN"
        rank_top.DWMRankingTop().start_rtn()

    elif mode == 'ira' or mode == '2':
        print pllc.SHELLHEAD + "check mode: illustRepoAll"
        illust_repo.IllustratorRepos().start_ira()

    elif mode == 'help':
        print pp.__doc__

    else:
        mode = None
        print pllc.SHELLHEAD + "argv(s) error\n"

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
