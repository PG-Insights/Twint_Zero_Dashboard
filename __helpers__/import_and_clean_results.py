#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 08:43:16 2023

@author: dale
"""


import sys
import pandas as pd
from pathlib import Path


HELPERS_DIR = Path(__file__).parent

if str(HELPERS_DIR) not in sys.path:
    sys.path.append(str(HELPERS_DIR))


class CleanResults:
    global HELPERS_DIR

    main_dir = HELPERS_DIR.parent
    twint_api_dir = Path(main_dir, 'Twint_API')
    twint_responses_dir = Path(twint_api_dir, 'twint-responses')

    @classmethod
    def _get_all_response_csv(cls) -> list:
        return [
            file for file in CleanResults.twint_responses_dir.iterdir()
            if 'csv' in Path(file).suffix
        ]

    @classmethod
    def _read_csv_and_combine(
            cls,
            list_of_paths: list) -> pd.DataFrame:
        def _read_csv(file: Path) -> pd.DataFrame:
            return pd.read_csv(
                str(file),
                usecols=[
                    'id', 
                    'url', 
                    'text', 
                    'username', 
                    'fullname', 
                    'timestamp',
                    'attachments', 
                    'stats'
                ],
                parse_dates=['timestamp']
            )
        return pd.concat(
            [_read_csv(file) for file in list_of_paths],
            axis=0,
        ).drop_duplicates(
            subset="id",
        ).set_index(
            'id',
            drop=True,
        )


if __name__ == '__main__':
    list_of_files = CleanResults._get_all_response_csv()
    df = CleanResults._read_csv_and_combine(list_of_files)
    for col in df.columns:
        print(df[col])