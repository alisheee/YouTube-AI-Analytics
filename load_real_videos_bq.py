import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime
from googleapiclient.discovery import build

# -----------------------------
# CONFIG
# -----------------------------
KEY_PATH = r"C:\Users\Asus VivoBook\Desktop\project\key_YT.json"
PROJECT_ID = "our-brand-487710-b8"
DATASET = "youtube_analytics"
TABLE = "raw_videos"

# -----------------------------
# AUTH
# -----------------------------
credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# -----------------------------
# YOUTUBE API
# -----------------------------
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
youtube_data = build("youtube", "v3", credentials=credentials)

# -----------------------------
# GET VIDEOS
# -----------------------------
videos_request = youtube_data.search().list(
    part="id,snippet",
    forMine=True,
    type="video",
    maxResults=50
)
videos_response = videos_request.execute()

videos_data = []
for item in videos_response.get("items", []):
    video_id = item["id"]["videoId"]
    title = item["snippet"]["title"]
    published = item["snippet"]["publishedAt"]

    stats_request = youtube_data.videos().list(
        part="statistics,contentDetails",
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
# LOAD TO BIGQUERY
# -----------------------------
table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"
job = client.load_table_from_dataframe(videos_df, table_id)
job.result()

print(f"{len(videos_df)} videos loaded successfully into BigQuery ✅")