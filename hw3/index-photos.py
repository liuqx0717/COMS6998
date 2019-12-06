import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
import requests
from requests_aws4auth import AWS4Auth
import boto3
import json
import uuid
import datetime


def detect_labels(photo, bucket):
    print("Connecting to rek...")
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10, MinConfidence=80)
    print("rek response = ", json.dumps(response, indent=2))
    label_list = [label['Name'].lower() for label in response['Labels']]
    return label_list


def lambda_handler(event, context):
    print("event = ", json.dumps(event, indent=2))
    records = event["Records"]
    for record in records:
        s3 = record["s3"]
        photo = s3["object"]["key"]
        bucket = s3["bucket"]["name"]
    label_list = detect_labels(photo, bucket)
    print("Labels detected: ", str(label_list))

    # es config
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
    # print("\nes_info = ", es.info())

    # index
    document = {
        "objectKey": photo,
        "bucket": bucket,
        "createdTimestamp": str(datetime.datetime.now()),
        "labels": label_list
    }
    print("document = ", json.dumps(document, indent=2))
    es.index(index="photos", doc_type="_doc", id=uuid.uuid4(), body=document)

    # res = es.search(index="photos", q="dog")
    # print("\nres = ", res, "\n")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

