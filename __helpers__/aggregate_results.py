#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 21:07:12 2023

@author: dale
"""

import sys
import pandas as pd
from pathlib import Path


HELPERS_DIR = Path(__file__).parent

if str(HELPERS_DIR) not in sys.path:
    sys.path.append(str(HELPERS_DIR))
    

class TwitterDataAgg:
    
    global HELPERS_DIR

    main_dir = HELPERS_DIR.parent
    twint_api_dir = Path(
        main_dir, 
        'Twint_API'
    )
    twint_responses_dir = Path(
        twint_api_dir, 
        'twint-responses'
    )
    
    def __init__(self):
        from import_and_clean_results import CleanResults
        self.df = CleanResults().df        
        self.stats_data = TwitterDataAgg._groupby_time_stats(self.df)


    @staticmethod
    def _groupby_time_stats(df: pd.DataFrame):
        return df.loc[
            ~df['fullname'].str.contains('Let MO Play')
        ].copy()[
            ['time', 'replies', 'retweets', 'quotes', 'likes']
        ].groupby(
            ['time'],
        ).sum()
    
    
if __name__ == '__main__':
    pass


















