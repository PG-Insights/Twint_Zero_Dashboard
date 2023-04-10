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

# Add the helpers directory to the system path if not present
if str(HELPERS_DIR) not in sys.path:
    sys.path.append(str(HELPERS_DIR))


class CleanResults:
    """
    A class to clean and consolidate Twitter data obtained
    from the Twint API.
    """

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
        list_of_files = CleanResults._get_all_response_csv()
        self.df = CleanResults._read_csv_and_combine(list_of_files)
        CleanResults.save_results(self.df)

    @classmethod
    def _get_all_response_csv(cls) -> list:
        """
        Get all CSV files in the twint_responses_dir.

        Returns:
            list: A list of file paths for all CSV files.
        """
        return [
            file for file in CleanResults.twint_responses_dir.iterdir()
            if 'csv' in Path(file).suffix
        ]

    @classmethod
    def _read_csv_and_combine(cls, list_of_paths: list) -> pd.DataFrame:
        """
        Read all CSV files from a list of paths and combine
        them into a single DataFrame.

        Args:
            list_of_paths (list): A list of file paths for all CSV files.

        Returns:
            pd.DataFrame: A DataFrame containing the combined CSV data.
        """

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
        ).reset_index(
            drop=True,
        )

    @classmethod
    def save_results(cls, df: pd.DataFrame) -> None:
        """
        Save the cleaned and consolidated DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
        """
        save_path = Path(cls.main_dir, 'db')
        save_path.mkdir(exist_ok=True)
        df.to_csv(
            str(
                Path(
                    save_path,
                    'all_twitter_results.csv'
                )
            ),
            index=False,
        )
