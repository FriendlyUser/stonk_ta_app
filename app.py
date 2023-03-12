import streamlit as st
import datetime
import pandas as pd
import requests
import os
import sys
from PIL import Image
from io import StringIO
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.common.technical_analysis.volatility_view import display_bbands, display_donchian

st.write("""
# Technical Analysis Web Application
Leveraging the openbb sdk, we can build a web application to display 
technical analysis graphs for any stock.
""")

st.sidebar.header('User Input Parameters')

today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.text_input("Ticker", 'ZIM')
    start_date = st.sidebar.text_input("Start Date", '2020-05-01')
    end_date = st.sidebar.text_input("End Date", f'{today}')
    # ta_range = st.sidebar.number_input("TA Range", min_value=1, max_value=50)
    return ticker, start_date, end_date # , ta_range

symbol, start, end = user_input_features()


def remove_existing_file(func):
    def wrapper(*args, **kwargs):
        old_stdin = sys.stdin
        sys.stdin = StringIO("y")
        stream = os.popen('cd ~ && pwd')
        root_dir = stream.read()
        sample_dir = root_dir.strip()
        # remove /home/codespace/OpenBBUserData/exports/bbands.png already
        # get last arg as export
        export = args[-1]
        temp_image = os.path.join(sample_dir, "OpenBBUserData", "exports", export)
        # if exists erase
        if os.path.exists(temp_image):
            os.remove(temp_image)
        func(*args, **kwargs)
        sys.stdin = old_stdin
        if os.path.exists(temp_image):
            return temp_image
        return None
    return wrapper

@remove_existing_file
@st.cache_data
def build_bbands_img(data, symbol, window=15, n_std=2, export="bbands.png"):
    return display_bbands(data, symbol, window, n_std, export=export)


@remove_existing_file
@st.cache_data
def build_donchian_img(data, symbol, export="donchian.png"):
    return display_donchian(data, symbol, export=export)
company_name = symbol.upper()

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# Read data 
data = load(symbol,start, 1440, end)
st.write(data)
# Adjusted Close Price
st.header(f"Adjusted Close Price\n {company_name}")
st.line_chart(data["Close"])

# get ta graph
bbands_img = build_bbands_img(data, symbol, 15, 2, "bbands.png")
# plot ta using open bb sdk in streamlit
st.header(f"Bollinger Bands")
# 
# if bbands.png exists, display it

if bbands_img:
    st.image(bbands_img, caption='Bollinger bands chart')

donchian_img = build_donchian_img(data, symbol, "donchian.png")
# plot ta using open bb sdk in streamlit
st.header(f"Donchian")

if donchian_img:
    st.image(donchian_img, caption='Donchian Openbb chart')
