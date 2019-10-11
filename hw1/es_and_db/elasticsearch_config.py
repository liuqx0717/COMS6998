from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from requests_aws4auth import AWS4Auth
import boto3
import json

host = 'search-e6998-dw4st2zsszipqnedjjfepbg47e.us-east-2.es.amazonaws.com'
region = 'us-east-2' 
service = 'es'
awsauth = AWS4Auth('AKIAJKMANSAMMSGXDOWA','OLFsgB24hSzxxVAl1Rgbkf1KwfhFG3su9VgRfy00', region, service) 

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

with open('/home/reuben/Downloads/mexican-es.json') as file:
    documents = json.load(file)

count=0
for i in documents:
    count+=1
    es.index(index="restaurants", doc_type="Restaurant", id=count, body=i)
