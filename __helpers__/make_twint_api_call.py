#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:36:30 2023

@author: dale
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

HELPERS_DIR = Path(__file__).parent

if str(HELPERS_DIR) not in sys.path:
    sys.path.append(str(HELPERS_DIR))
    

class TwintController:
    global HELPERS_DIR
    
    main_dir = Path(HELPERS_DIR).parent
    twint_dir = Path(main_dir, 'Twint_API')
    twint_responses_dir = Path(twint_dir, 'twint-responses')
    
    recent_responses = None
    
    if str(twint_dir) not in sys.path:
        sys.path.append(str(twint_dir))
        
    def __init__(self):
        if TwintController.recent_responses is None:
            self._make_twint_api_call()
            self._set_recent_response()
        TwintController.recent_responses = TwintController._filter_all_responses(
            TwintController.recent_responses
        )
        if len(TwintController.recent_responses) < 1:
            self._make_twint_api_call()
        self._set_recent_response()
            
    
    @classmethod
    def _get_all_response_files(cls) -> list:
        return [
            file for file in cls.twint_responses_dir.iterdir()
            if file.is_file()
        ]

    @staticmethod
    def _filter_all_responses(files_list: list) -> list:
        one_hour_ago = datetime.now() - timedelta(hours=1)
        return [
            file for file in files_list if 
            datetime.fromtimestamp(Path(file).stat().st_mtime) > one_hour_ago
        ]
    
    def _set_recent_response(self):
        self.twint_responses_list = TwintController._get_all_response_files()
        TwintController.recent_responses = self._filter_all_responses(
            self.twint_responses_list
        )
        
    def _make_twint_api_call(self):
        from twint_api import TwintApi 
        TwintApi()
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    