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
        self.lmp_tweets = TwitterDataAgg._return_only_lmp_tweets(
            self.df
        )
        self.non_lmp_tweets = TwitterDataAgg._return_non_lmp_tweets(
            self.df
        )
        self.all_stats = TwitterDataAgg._groupby_time_stats(
            self.df
        )
        self.lmp_stats = TwitterDataAgg._groupby_time_stats(
            self.lmp_tweets
        )
        self.non_lmp_stats = TwitterDataAgg._groupby_time_stats(
            self.non_lmp_tweets
        )

    @staticmethod
    def _return_only_lmp_tweets(df: pd.DataFrame) -> None:
        return df.loc[
            df['fullname'].str.contains('Let MO Play')
        ].copy()
        
    @staticmethod
    def _return_non_lmp_tweets(df: pd.DataFrame) -> None:
        return df.loc[
            ~df['fullname'].str.contains('Let MO Play')
        ].copy()

    @staticmethod
    def _groupby_time_stats(df: pd.DataFrame):
        return df.copy()[
            ['Date & Hour', 'replies', 'retweets', 'quotes', 'likes']
        ].groupby(
            ['Date & Hour'],
        ).sum()
    
    
if __name__ == '__main__':
    obj = TwitterDataAgg()
    print(obj.all_stats)

















