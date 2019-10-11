from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from requests_aws4auth import AWS4Auth
import boto3
import json

# Input restaurant category HERE:
# category = "japanese"
category= json.loads(requests.get())['body']['Item']

# aws es setup
host = 'search-e6998-dw4st2zsszipqnedjjfepbg47e.us-east-2.es.amazonaws.com'  # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-2'  # e.g. us-west-1
service = 'es'
awsauth = AWS4Auth('AKIAJKMANSAMMSGXDOWA', 'OLFsgB24hSzxxVAl1Rgbkf1KwfhFG3su9VgRfy00', region, service)

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# ElasticSearch: Random search with 'seed'
payload = {
    "size": 1,
    "query": {
        "function_score": {
            "functions": [
                {"filter": {"term": {"categories": "init"}}, "weight": "1"},
                {"random_score": {"seed": "0"}}
            ],
            "score_mode": "sum"
        }
    }
}

payload["query"]["function_score"]["functions"][0]["filter"]["term"]["categories"] = category

while 1:
    payload["query"]["function_score"]["functions"][1]["random_score"]["seed"] += 1
    r = requests.get(
        "https://search-e6998-dw4st2zsszipqnedjjfepbg47e.us-east-2.es.amazonaws.com/restaurants/Restaurant"
        "/_search",
        headers={"Content-Type": "application/json"},
        json=payload)
    es_response = json.loads(r.text)
    business_id = es_response["hits"]["hits"][0]["_source"]["business_id"]
    if business_id != "#NAME?":  # Due to defects of orignal dataset, some "business_id" is "#NAME?". Do another search if so.
        break

# query in dynamodb:
client = boto3.client('dynamodb', aws_access_key_id='AKIAJKMANSAMMSGXDOWA',
                      aws_secret_access_key='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', region_name='us-east-2')
query_key = {
    "business_id": {
        "S": "init",
    },
}

query_key["business_id"]["S"]=business_id

db_response = client.get_item(Key=query_key, TableName="yelp-restaurants")

# lambda handler
def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': db_response["Item"] # json.dumps(response)
    }
