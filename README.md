# alpaca-stream

This project streams stock quotes from Alpaca to AWS Kinesis Firehose, and storing the data in S3, which can be crawled by AWS Glue and queried by AWS Athena for downstream analysis.

Install these dependencies using pip3 install:

websocket-client
boto3

You also need to create a AWS Kinesis Firehose stream before running stream.py.

To run:
python3 stream.py

Alpaca API Doc:
https://alpaca.markets/docs/api-documentation/api-v2/market-data/alpaca-data-api-v2/real-time/#data-points
