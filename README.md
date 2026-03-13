# 📺 YouTube AI Analytics Assistant

An AI-powered analytics assistant that allows you to explore YouTube channel data using **natural language queries**.

This project integrates **YouTube API, BigQuery, OpenAI, and Streamlit** to create an interactive analytics tool.

Instead of writing SQL manually, users can simply ask questions like:

* "Top 5 videos by views"
* "Where does my audience come from?"
* "Which traffic source dominates?"
* "How many subscribers did I gain?"

The system automatically:

1. Converts the question into **BigQuery SQL**
2. Executes the query
3. Returns structured results
4. Generates **AI insights**

---

# 🚀 Demo Example

User asks:

> Top 5 videos

Assistant returns:

<img width="639" height="739" alt="Image" src="data_pipeline/screen" />


💡 **Insight**

The most popular videos on the channel are anime-related clips and music edits. These formats significantly outperform other content types in terms of views.

---

# 🧠 Architecture

```
User Question
      │
      ▼
Streamlit Chat Interface
      │
      ▼
OpenAI (SQL generation)
      │
      ▼
BigQuery
      │
      ▼
Pandas DataFrame
      │
      ▼
OpenAI (Insight generation)
      │
      ▼
Streamlit response
```

---

# ⚙️ Tech Stack

### Data

* Google BigQuery
* YouTube Analytics API

### AI

* OpenAI GPT models

### Backend

* Python
* Pandas

### Interface

* Streamlit

---

# 📂 Project Structure

```
youtube-ai-analytics
│
├── data_pipeline
│   ├── app.py                # Streamlit chat interface
│   ├── llm_utils.py          # OpenAI integration
│   ├── bq_utils.py           # BigQuery client
│   ├── sql_generator.py      # SQL generation logic
│   └── load_youtube_bq.py    # Load YouTube data to BigQuery
│
├── scripts
│   ├── load_youtube_to_bq.py
│   └── load_real_videos_bq.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 📊 Dataset

YouTube analytics data is stored in **Google BigQuery**.

### raw_videos

| column       | description        |
| ------------ | ------------------ |
| video_id     | YouTube video ID   |
| title        | video title        |
| published_at | publish date       |
| views        | total views        |
| likes        | number of likes    |
| comments     | number of comments |

---

### raw_channel_overview

Daily channel statistics including:

* views
* watch time
* subscriber growth

---

### raw_traffic

Traffic sources:

* YouTube search
* Browse features
* Suggested videos
* External sources

---

### raw_geo

Audience distribution by **country**.

---

### raw_device

Viewer devices:

* mobile
* desktop
* tablet
* TV

---

# 🤖 AI Features

## Natural Language Queries

Users can ask analytics questions without writing SQL.

Example:

```
Top 10 videos by likes
```

AI automatically generates a query like:

```
SELECT title, likes
FROM youtube_analytics.raw_videos
ORDER BY likes DESC
LIMIT 10
```

---

## AI-generated Insights

After retrieving the data, the system generates a **human-readable analysis** explaining the results.

Example insight:

> Most traffic comes from YouTube search, which suggests the videos are well optimized for keywords and discovery.

---

# 📈 Example Questions

Users can ask:

```
Top 5 videos
```

```
Where does my audience come from?
```

```
Which device is used most by viewers?
```

```
How many subscribers did I gain?
```

```
What traffic source dominates?
```

---

# 🛠 Installation

Clone repository:

```
git clone https://github.com/your-username/youtube-ai-analytics.git
cd youtube-ai-analytics
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the Streamlit app:

```
streamlit run data_pipeline/app.py
```

---

# 🔑 Configuration

You need to provide your own credentials:

```
key_YT.json
OpenAI.json
credentials_oauth.json
token.json
```

These files contain API keys and **must not be uploaded to GitHub**.
They are excluded via `.gitignore`.

---

# 📊 Future Improvements

Planned features:

* 📈 automatic chart generation
* 🔎 semantic search across video titles
* 📊 audience growth forecasting
* 🎥 AI recommendations for future videos

---

# 👨‍💻 Author

AI / Data enthusiast building analytics tools with Python, cloud technologies, and machine learning.

---

# ⭐ If you like the project

Consider giving the repository a star ⭐
