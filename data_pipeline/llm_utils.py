import json
import pandas as pd
import re
from openai import OpenAI
from google.cloud import bigquery

# -----------------------------
# CONFIG
# -----------------------------
OPENAI_PATH = r"C:\Users\Asus VivoBook\Desktop\project\OpenAI.json"
DATASET = "youtube_analytics"

# -----------------------------
# LOAD OPENAI KEY
# -----------------------------
with open(OPENAI_PATH, "r") as f:
    api_data = json.load(f)

client_openai = OpenAI(api_key=api_data["api_key"])

# -----------------------------
# SCHEMA CONTEXT (CRITICAL)
# -----------------------------
SCHEMA_CONTEXT = f"""
You are a BigQuery SQL expert.
Dataset: {DATASET}

Tables and Columns:
- raw_videos: video_id (STRING), title (STRING), published_at (TIMESTAMP), views (INTEGER), likes (INTEGER), comments (INTEGER)
- raw_channel_overview: date (DATE), views (INTEGER), watch_time_min (INTEGER), avg_view_duration (FLOAT), subs_gained (INTEGER), subs_lost (INTEGER)
- raw_traffic: traffic_source (STRING), views (INTEGER)
- raw_geo: country (STRING), views (INTEGER)
- raw_device: device_type (STRING), views (INTEGER)

Return ONLY valid BigQuery SQL. Do NOT explain anything.
"""

# -----------------------------
# GENERATE SQL VIA OPENAI
# -----------------------------
def generate_sql(question: str):
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SCHEMA_CONTEXT +
                "\nReturn ONLY raw BigQuery SQL. No markdown. No explanations. No ``` blocks."
            },
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content

    # Aggressive markdown cleanup
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()

    return sql

# -----------------------------
# EXECUTE QUERY
# -----------------------------
def execute_sql(client: bigquery.Client, sql: str):
    query_job = client.query(sql)
    df = query_job.to_dataframe()
    return df

# -----------------------------
# GENERATE INSIGHT
# -----------------------------
def generate_insight(question: str, df: pd.DataFrame):
    """
    Generates a human-friendly explanation of the data.
    Note: The AI is instructed to respond in English as per original logic.
    """
    if df.empty:
        return "No data found 🔍"

    data_preview = df.head(10).to_string()

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are a YouTube Channel Analyst.
You will receive the results of a SQL query.
Explain the results in SIMPLE English (as per user preference).
No SQL. No technical jargon. 
Be concise and highlight key trends.
"""
            },
            {
                "role": "user",
                "content": f"""
User Question: {question}
Table Result:
{data_preview}
"""
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()