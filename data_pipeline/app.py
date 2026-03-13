import streamlit as st
from llm_utils import generate_sql, execute_sql, generate_insight  # Оновлено назву імпорту
from google.cloud import bigquery
from google.oauth2 import service_account

# -------------------------
# BIGQUERY CLIENT
# -------------------------
def get_bq_client():
    # Ensure the key_YT.json file is in the same directory as the script
    credentials = service_account.Credentials.from_service_account_file(
        "key_YT.json"
    )

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id
    )

    return client

client = get_bq_client()

# -------------------------
# STREAMLIT UI
# -------------------------
st.set_page_config(
    page_title="YouTube AI Assistant",
    page_icon="📊"
)

st.title("📺 YouTube Chat Analytics")

# -------------------------
# CHAT HISTORY
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display dataframe from history if it exists
        if "df" in message:
            # hide_index=True hides the system column with 0, 1, 2...
            st.dataframe(message["df"], use_container_width=True, hide_index=True)

# -------------------------
# USER INPUT
# -------------------------
if prompt := st.chat_input("Ask something about the channel or videos..."):

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        try:
            # 1. GENERATE SQL
            sql = generate_sql(prompt)

            # 2. EXECUTE SQL
            df = execute_sql(client, sql)

            # Check for results
            if df is None or df.empty:
                response = "🔍 No data found. Please try rephrasing your request."
                st.markdown(response)
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            else:
                # 3. ADD ROW NUMBER COLUMN
                # Create numbering starting from 1
                df.insert(0, "#", range(1, len(df) + 1))

                # 4. GENERATE INSIGHT
                insight = generate_insight(prompt, df)

                st.markdown("### 📈 Data for your request")
                
                # IMPORTANT: hide_index=True removes duplicate numbering
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.markdown(f"### 💡 Comment\n{insight}")

                # Save response along with the dataframe to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"💡 **Comment:** {insight}",
                    "df": df
                })

        except Exception as e:
            error_msg = f"⚠️ Failed to process request: {str(e)}"
            st.error(error_msg)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })