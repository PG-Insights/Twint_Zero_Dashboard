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
        temp_df = CleanResults._read_csv_and_combine(list_of_files)
        temp_df = CleanResults._expand_stats_col(temp_df)
        self.df = CleanResults._time_col_timestamp_type(temp_df)
        self._insert_time_col()
        self._insert_date_col()

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
                dtype={
                    'id': str,
                    'url': str,
                    'text': str,
                    'username': str,
                    'fullname': str,
                },
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

    @staticmethod
    def _expand_stats_col(df: pd.DataFrame) -> pd.DataFrame:
        import ast

        def string_to_dataframe(s):
            d = ast.literal_eval(s)
            df = pd.DataFrame([d])
            return df

        temp_1 = pd.DataFrame()
        for row in df['stats'].values:
            temp_1 = pd.concat(
                [temp_1, string_to_dataframe(row)],
                axis=0
            )
        temp_data = temp_1.reset_index(drop=True)
        temp_2 = df.copy().drop(columns=['stats'])
        return pd.concat(
            [temp_2, temp_data],
            axis=1,
        )

    @staticmethod
    def _time_col_timestamp_type(
            df: pd.DataFrame,
            col_name='timestamp') -> pd.DataFrame:
        from datetime import datetime
        
        def parse_datetime_string(datetime_string):
            dt = datetime.strptime(datetime_string, "%b %d, %Y · %I:%M %p %Z")
            return pd.Timestamp(dt)

        if col_name:
            df[col_name] = df[col_name].apply(parse_datetime_string)
        else:
            df = df.applymap(parse_datetime_string)
        return df

    @staticmethod
    def _get_hour_col_from_timestamp(
            df: pd.DataFrame,
            dt_col='timestamp') -> pd.Series:
        return df[dt_col].copy().apply(lambda x: (x.time()).hour)
    
    def _insert_time_col(self) -> None:
        self.df.insert(
            len(self.df.columns),
            'time',
            CleanResults._get_hour_col_from_timestamp(self.df)
        )
        
    def _insert_date_col(self) -> None:
        self.df.insert(
            len(self.df.columns),
            'date',
            self.df['timestamp'].dt.date.values
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
