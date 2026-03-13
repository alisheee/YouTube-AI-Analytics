def generate_sql(question: str):

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SCHEMA_CONTEXT + "\nReturn ONLY raw BigQuery SQL without markdown formatting and without ``` blocks."
            },
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # 🔥 Видаляємо markdown якщо модель його додала
    if sql.startswith("```"):
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql