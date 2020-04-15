from google.cloud import bigquery
import pandas


def main():
  # initialise BigQuery client
  client = bigquery.Client()

  # get bitcoin data
  getTable(client, "crypto_bitcoin", "blocks")
  getTable(client, "crypto_bitcoin", "inputs")
  getTable(client, "crypto_bitcoin", "outputs")
  getTable(client, "crypto_bitcoin", "transactions")


def getTable(client, dataset, table):
  QUERY = "SELECT * FROM `bigquery-public-data." + dataset + "." + table + "` LIMIT 100"
  query_job = client.query(QUERY) 
  rows = query_job.result()  
  df = rows.to_dataframe()
  df.to_csv("../Data/BigQueryData/" + dataset + "_" + table + ".csv")


if __name__== "__main__":
  main()