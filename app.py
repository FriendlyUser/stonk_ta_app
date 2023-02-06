import streamlit as st
import datetime
import pandas as pd
import requests
import os
from PIL import Image
from openbb_terminal.stocks.stocks_helper import load
from openbb_terminal.common.technical_analysis.volatility_model import bbands
from openbb_terminal.common.technical_analysis.volatility_view import display_bbands

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


@st.cache  # 👈 Added this
def build_bbands_img(data, symbol, file_name="sample.png"):
    stream = os.popen('cd ~ && pwd')
    root_dir = stream.read()
    sample_dir = root_dir.strip()
    # remove /home/codespace/OpenBBUserData/exports/bbands.png already
    temp_image = os.path.join(sample_dir, "OpenBBUserData", "exports", file_name)
    # if exists erase
    if os.path.exists(temp_image):
        os.remove(temp_image)
    display_bbands(data, symbol, 15, 2, export=file_name)
    # root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    temp_image = os.path.join(sample_dir, "OpenBBUserData", "exports", file_name)
    # image = Image.open(temp_image)
    return temp_image

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
bbands_img = build_bbands_img(data, symbol, "bbands.png")
# plot ta using open bb sdk in streamlit
st.header(f"Bollinger Bands\n {company_name}")
# 
# if bbands.png exists, display it

if bbands_img:
    st.image(bbands_img, caption='Sunrise by the mountains')
