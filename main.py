#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 08:47:37 2023

@author: dale
"""

import sys
import streamlit as st
from pathlib import Path
import plotly.express as px

MAIN_DIR = Path(__file__).parent

if str(MAIN_DIR) not in sys.path:
    sys.path.append(str(MAIN_DIR))
    
    
def _get_all_results():
    from __helpers__.aggregate_results import TwitterDataAgg
    return TwitterDataAgg()


def main():
    st.header('Twitter Data - Twint_Zero_Dashboard')
    data = _get_all_results()
    st.dataframe(data.df)
    st.plotly_chart(px.line(data.stats_data))


if __name__ == '__main__':
    main()