from google.cloud import bigquery
import pandas

def main():
    client = bigquery.Client()
    QUERY = 'SELECT * FROM `bigquery-public-data.crypto_bitcoin.blocks` LIMIT 100'
    query_job = client.query(QUERY) 
    rows = query_job.result()  
    df = rows.to_dataframe()
    df.to_csv("./BigQueryData/crypto_bitcoin.csv")

if __name__== "__main__":
  main()