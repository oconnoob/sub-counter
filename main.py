
import os
import time
import math

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

key = os.getenv('KEY')
aai_channel_id = os.getenv('CHANNEL_ID')

# yt api limits
seconds_per_day = 60*60*24
units_per_day = 10000
min_seconds_per_unit = math.ceil(seconds_per_day/units_per_day)
units_per_call = 1
min_seconds_per_call = min_seconds_per_unit * units_per_call

# ensure that the p
polling_rate = 15
polling_rate = max(polling_rate, min_seconds_per_call)

################# API CLIENT
api_service_name = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version,  developerKey=key)

################ SUBS CACHE
@st.cache_data(ttl=polling_rate)
def update_current_subs():
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=aai_channel_id
    )
    response = request.execute()
    return response['items'][0]['statistics']['subscriberCount']


###### streamlit app #############
st.set_page_config(page_title="Sub count", page_icon='logo.png', layout="centered", initial_sidebar_state="auto", menu_items=None)

subs = update_current_subs()

st.title("AssemblyAI YouTube subscriber count 🎉")
st.header(subs)

time.sleep(5)
st.rerun()