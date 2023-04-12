#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:45:15 2023

@author: dale
"""

import json
import argparse
import subprocess
import pandas as pd
from os import chdir
from pathlib import Path
from datetime import datetime

TWINT_API_DIR = Path(__file__).parent


def create_query(*args):
    """
    Creates a query by joining arguments.

    Returns:
        str: The combined query string.
    """
    if len([arg for arg in args]) > 1:
        return ' '.join(*args)
    else:
        return args


def return_query_results(
    query: str
) -> subprocess:
    """
    Runs a subprocess to execute the Twint Zero API query.

    Args:
        query (str): The Twitter query string.

    Returns:
        subprocess: The subprocess output containing the JSON data.
    """
    global TWINT_API_DIR
    chdir(TWINT_API_DIR)
    cmd = [
        'go',
        'run',
        'main.go',
        '-Query',
        query,
        '-Instance',
        'birdsite.xanny.family',
        '-Format',
        'json',
    ]
    # If Instance needs to be modified use a value from https://github.com/zedeus/nitter/wiki/Instances

    process = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return process.stdout


def parse_json_returned(json_str: str) -> json:
    """
    Parses the returned JSON string.

    Args:
        json_str (str): The JSON string returned by the subprocess.

    Returns:
        json: The parsed JSON object.
    """
    return json.loads(
        json.JSONEncoder().encode(
            json_str
        )
    )

class TwintApi:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Run "Twint Zero" API Twitter Query'
        )
        parser.add_argument(
            'query',
            nargs='?',
            default='to:LetMOPLay within_time:72h filter:has_engagement lang:en',
            help='Twitter query string: https://github.com/igorbrigadir/twitter-advanced-search'
        )
        args = parser.parse_args()
        query_str = args.query
        json_str = return_query_results(
            query_str,
        )
        response_json = parse_json_returned(
            json_str
        )
        df = pd.read_json(
            response_json,
            lines=True
        )
        response_dir = Path(
            TWINT_API_DIR,
            'twint-responses'
        )
        response_dir.mkdir(exist_ok=True)
        save_name = f'{datetime.now()}_{query_str}'
        df.to_csv(
            Path(
                response_dir,
                f'{save_name}.csv'
            ),
            index=False,
        )
        print(f'\nExport name: {save_name}\n')


if __name__ == '__main__':
    TwintApi()
    
