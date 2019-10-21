#from googleapiclient.discovery import build
from google.cloud import bigquery

# def main():
#     service = build("bigquery", "v2")
#     datasets = service.datasets()
#     print(datasets.get(projectId="bigquery-public-data", datasetId="crypto_bitcoin").execute())

def main():
    client = bigquery.Client()

    QUERY = 'SELECT * FROM `bigquery-public-data.crypto_bitcoin.blocks` LIMIT 100'

    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row)

if __name__== "__main__":
  main()