import json
import boto3

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))
    records = event["Records"]
    for record in records:
        s3 = record["s3"]
        photo = s3["object"]["key"]
        bucket = s3["bucket"]["name"]
    label_list=detect_labels(photo, bucket)
    print("Labels detected: ", str(label_list))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def detect_labels(photo, bucket):

    client=boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=10, MinConfidence=80)
    
    label_list = [label['Name'].lower() for label in response['Labels']]
    return label_list

