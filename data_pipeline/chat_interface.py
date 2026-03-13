from bq_utils import get_bq_client
from llm_utils import generate_sql, execute_sql, generate_insight # Оновлено назву функції

KEY_PATH = r"C:\Users\Asus VivoBook\Desktop\project\key_YT.json"
PROJECT_ID = "our-brand-487710-b8"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

def run_chat(client):
    print("AI YouTube Chat Ready 🤖 (type '1' to quit)")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "1":
            print("Goodbye 👋")
            break

        if not user_input:
            continue

        try:
            # 1️⃣ Generate SQL via LLM
            sql = generate_sql(user_input)
            
            # 2️⃣ Execute SQL
            df = execute_sql(client, sql)

            # 3️⃣ If no results found → search for similar titles (Fallback)
            if df.empty:
                print("AI: No exact matches found 🔍 searching for similar videos...")

                # Clean input for safe SQL searching
                search_term = user_input.replace("'", "''")
                fallback_sql = f"""
                SELECT video_id, title, views
                FROM youtube_analytics.raw_videos
                WHERE LOWER(title) LIKE LOWER('%{search_term}%')
                ORDER BY views DESC
                LIMIT 5;
                """
                df = execute_sql(client, fallback_sql)

                if df.empty:
                    print("AI: No similar videos found either ❌")
                    continue

            # 4️⃣ Display results
            print("\n📊 Results Table:")
            print(df.to_string(index=True))

            # 5️⃣ Generate insight based on the retrieved data
            insight = generate_insight(user_input, df)
            print("\n💡 Assistant's Insight:")
            print(insight)

        except Exception as e:
            print("\n⚠️ Oops, something went wrong while processing your request 🤖")
            print("Reason:", str(e))
            continue