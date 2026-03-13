import os
import pickle
from datetime import datetime
import pandas as pd

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.cloud import bigquery
from google.oauth2 import service_account

# -----------------------------
# CONFIG
# -----------------------------
YOUTUBE_OAUTH_PATH = r"C:\Users\Asus VivoBook\Desktop\project\credentials_oauth.json"
TOKEN_PATH = r"C:\Users\Asus VivoBook\Desktop\project\token.json"
BQ_KEY_PATH = r"C:\Users\Asus VivoBook\Desktop\project\key_YT.json"
PROJECT_ID = "our-brand-487710-b8"
DATASET = "youtube_analytics"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

# -----------------------------
# AUTH: YouTube (OAuth2 + token.json)
# -----------------------------
creds = None
if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH, "rb") as token_file:
        creds = pickle.load(token_file)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_OAUTH_PATH, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save credentials for next run
    with open(TOKEN_PATH, "wb") as token_file:
        pickle.dump(creds, token_file)

youtube_data = build("youtube", "v3", credentials=creds)
youtube_analytics = build("youtubeAnalytics", "v2", credentials=creds)

# -----------------------------
# SERVICE ACCOUNT FOR BQ
# -----------------------------
bq_credentials = service_account.Credentials.from_service_account_file(BQ_KEY_PATH)
bq_client = bigquery.Client(credentials=bq_credentials, project=PROJECT_ID)

# -----------------------------
# HELPER: LOAD TO BIGQUERY
# -----------------------------
def load_to_bq(df, table_name):
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    bq_client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config
    ).result()

    print(f"{len(df)} rows overwritten in {table_name} ✅")

# -----------------------------
# 1️⃣ Videos
# -----------------------------
videos_request = youtube_data.search().list(
    part="id,snippet",
    forMine=True,
    type="video",
    maxResults=500
)
videos_response = videos_request.execute()

videos_data = []
for item in videos_response.get("items", []):
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    published = item["snippet"]["publishedAt"]

    stats_request = youtube_data.videos().list(
        part="statistics",
        id=video_id
    )
    stats_response = stats_request.execute()
    stats = stats_response["items"][0]["statistics"]

    view_count = int(stats.get("viewCount", 0))
    like_count = int(stats.get("likeCount", 0))
    comment_count = int(stats.get("commentCount", 0))

    videos_data.append([video_id, title, published, view_count, like_count, comment_count])

videos_df = pd.DataFrame(
    videos_data,
    columns=["video_id", "title", "published_at", "views", "likes", "comments"]
)

# -----------------------------
# 2️⃣ Channel Overview (daily)
# -----------------------------
overview_request = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate="2022-01-01",
    endDate=datetime.today().strftime("%Y-%m-%d"),
    metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost",
    dimensions="day",
    sort="day"
)
overview_response = overview_request.execute()

overview_df = pd.DataFrame(
    overview_response.get("rows", []),
    columns=["date", "views", "watch_time_min", "avg_view_duration", "subs_gained", "subs_lost"]
)
# -----------------------------
# 3️⃣ Traffic Sources
# -----------------------------
traffic_request = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate="2022-01-01",
    endDate=datetime.today().strftime("%Y-%m-%d"),
    metrics="views",
    dimensions="insightTrafficSourceType"
)
traffic_response = traffic_request.execute()

traffic_df = pd.DataFrame(
    traffic_response.get("rows", []),
    columns=["traffic_source", "views"]
)
# -----------------------------
# 4️⃣ GEO
# -----------------------------
geo_request = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate="2025-01-01",
    endDate=datetime.today().strftime("%Y-%m-%d"),
    metrics="views",
    dimensions="country"
)
geo_response = geo_request.execute()

geo_df = pd.DataFrame(
    geo_response.get("rows", []),
    columns=["country", "views"]
)
# -----------------------------
# 5️⃣ Device Types
# -----------------------------
device_request = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate="2025-01-01",
    endDate=datetime.today().strftime("%Y-%m-%d"),
    metrics="views",
    dimensions="deviceType"
)
device_response = device_request.execute()

device_df = pd.DataFrame(
    device_response.get("rows", []),
    columns=["device_type", "views"]
)


load_to_bq(videos_df, "raw_videos")
load_to_bq(overview_df, "raw_channel_overview")
load_to_bq(traffic_df, "raw_traffic")
load_to_bq(geo_df, "raw_geo")
load_to_bq(device_df, "raw_device")



print("✅ All 5 tables loaded into BigQuery successfully!")