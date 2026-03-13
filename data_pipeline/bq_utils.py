from google.cloud import bigquery
import pandas as pd

def get_bq_client(key_path: str, project_id: str):
    return bigquery.Client.from_service_account_json(key_path, project=project_id)

def run_query(client, query: str) -> pd.DataFrame:
    df = client.query(query).to_dataframe()
    return df