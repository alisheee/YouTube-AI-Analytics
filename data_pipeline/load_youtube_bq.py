import os
import pickle
from datetime import datetime
import pandas as pd

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from .bq_utils import get_bq_client, load_df_to_bq

# -----------------------------
# CONFIG
# -----------------------------
YOUTUBE_OAUTH_PATH = r"../credentials_oauth.json"
TOKEN_PATH = r"../token.json"
BQ_KEY_PATH = r"../key_YT.json"
PROJECT_ID = "our-brand-487710-b8"
DATASET = "youtube_analytics"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

# -----------------------------
# YouTube OAuth + token.json
# -----------------------------
creds = None
if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_OAUTH_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(TOKEN_PATH, "wb") as f:
        pickle.dump(creds, f)

youtube_data = build("youtube", "v3", credentials=creds)
youtube_analytics = build("youtubeAnalytics", "v2", credentials=creds)

# -----------------------------
# BigQuery client
# -----------------------------
bq_client = get_bq_client(BQ_KEY_PATH, PROJECT_ID)

# -----------------------------
# videos_df, overview_df, traffic_df, geo_df, device_df
# -----------------------------
# load_df_to_bq(bq_client, videos_df, DATASET, "raw_videos")
# load_df_to_bq(bq_client, overview_df, DATASET, "raw_channel_overview")
# load_df_to_bq(bq_client, traffic_df, DATASET, "raw_traffic")
# load_df_to_bq(bq_client, geo_df, DATASET, "raw_geo")
# load_df_to_bq(bq_client, device_df, DATASET, "raw_device")
