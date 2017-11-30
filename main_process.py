#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# code by </MATRIX>@Neod Anderjon(LeaderN)
# =====================================================================
# this python script is built to run main process

import pllc, priv_lib, rank_top, illust_repo                        # call private lib

pllc.encode_resolve()

if __name__ == '__main__':
    print priv_lib.Matrix().__doc__
    mode = raw_input(pllc.SHELLHEAD + 'select a mode: ')            # choose mode
    if mode == 'rtn' or mode == '1':
        print pllc.SHELLHEAD + "check mode: RankTopN"
        rtn_work = rank_top.DWMRankingTop(pllc.ranking_folder,
                                          pllc.logfile_path,
                                          pllc.htmlfile_path)
        rtn_work.start()
    elif mode == 'ira' or mode == '2':
        print pllc.SHELLHEAD + "check mode: illustRepoAll"
        global_id = raw_input(pllc.SHELLHEAD
                  + 'target crawl illustrator pixiv-id: ')
        ira_work = illust_repo.IllustratorRepos(global_id,
                                         pllc.work_dir,
                                         pllc.logfile_name,
                                         pllc.htmlfile_name)
        ira_work.start()
    elif mode == 'help':
        print priv_lib.Matrix().__doc__
    else:
        print pllc.SHELLHEAD + "argv(s) error\n"

# =====================================================================
# code by </MATRIX>@Neod Anderjon(LeaderN)
