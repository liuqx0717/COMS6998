import boto3
import json

with open('/home/reuben/Downloads/mexican-put.json') as file:
    items = json.load(file)

client = boto3.client('dynamodb',aws_access_key_id='AKIAJKMANSAMMSGXDOWA', aws_secret_access_key='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', region_name='us-east-2')

for i in items:
    response = client.put_item(
        Item=i,
        ReturnConsumedCapacity='TOTAL',
        TableName='yelp-restaurants'
    )
    print(response)
