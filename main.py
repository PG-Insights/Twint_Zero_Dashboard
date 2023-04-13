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
    from __helpers__.make_twint_api_call import TwintController 
    TwintController()
    return TwitterDataAgg()


def _select_results_df_to_view() -> str:
    option_selected = st.selectbox(
        'Select Results to View',
        [
            'All Results',
            'LMP Posts Only',
            'Non LMP Posts Only',
        ]
    )
    return option_selected
    

def _display_results_plot(data_obj, selected=None):
    if selected == 'All Results':
        return data_obj.all_stats
    elif selected == 'Non LMP Posts Only':
        return data_obj.non_lmp_stats
    else: 
        return data_obj.lmp_stats 


def _display_max_results_as_metrics(data_df):
    max_df = data_df.max()
    cols = st.columns(len(max_df))
    for i, col in enumerate(max_df.index):
        with cols[i]:
            st.metric(
                col,
                value=max_df[col]
            )

def main():
    st.header('Twitter Data - Twint_Zero_Dashboard')
    data_container = st.container()
    options_container = st.container()
    data_obj = _get_all_results()
    with options_container:
        option_selected = _select_results_df_to_view()
    with data_container:
        data_df = _display_results_plot(
            data_obj,
            selected=option_selected,
        )
        st.plotly_chart(
            px.line(data_df),
            use_container_width=True,
        )
        st.subheader('Max responses in data')
        _display_max_results_as_metrics(data_df)


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    main()