from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from requests_aws4auth import AWS4Auth
import boto3
import json
import uuid
import datetime

host = 'vpc-photos-rxqmfbkp3mzqjkteqaecvpkmtm.us-east-1.es.amazonaws.com'
region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

event = {'Records': [
    {'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2019-12-05T21:21:53.818Z',
     'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'A3TRS0B5U108UU'},
     'requestParameters': {'sourceIPAddress': '160.39.165.13'},
     'responseElements': {'x-amz-request-id': '09A84B8D2C4090B3',
                          'x-amz-id-2': 'JPas9nv/JMXpNJ1JhBDMkXsyKz6V0BZWd0wHS6khcTGXUQp6uJ2ujf0Ob6jUcWlopL7eo+Lhc5A='},
     's3': {'s3SchemaVersion': '1.0', 'configurationId': 'PutPhoto',
            'bucket': {'name': 'photobucket0', 'ownerIdentity': {'principalId': 'A3TRS0B5U108UU'},
                       'arn': 'arn:aws:s3:::photobucket0'},
            'object': {'key': 'Untitled-1.jpg', 'size': 272852, 'eTag': '811f924324c5ecb51779fa6fd3d8550f',
                       'sequencer': '005DE974F1BB100A8B'}}}]}

print("timestamp = ", datetime.datetime.now().timestamp())

document = {
    "objectKey": "my-photo.jpg",
    "bucket": "my-photo-bucket",
    "createdTimestamp": "2018-11-05T12:40:02",
    "labels": [
        "person",
        "dog",
        "ball",
        "park"
    ]
}

es.index(index="photos", doc_type="_doc", id=uuid.uuid4(), body=document)
