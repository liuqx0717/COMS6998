import boto3
import json
client = boto3.client('lex-runtime', region_name='us-east-1')


def get_response(event):
    query = event['query']
    userId = event['userId']
    resp = ask_lex(query, userId)['ResponseMetadata']['HTTPHeaders']['x-amz-lex-message']
    # print("&&&")
    # print(event)
    
    return json.dumps({'sessionid':userId, 'content':resp}).encode('utf-8')
    # return json.dumps(event).encode('utf-8')


def ask_lex(query, userId):
    resp = client.post_content(
        botName='DiningBot',
        botAlias='DiningBotBETA',
        userId=userId,
        sessionAttributes={},
        contentType="text/plain; charset=utf-8",
        inputStream=query

    )
    return resp


def lambda_handler(event, context):
    return get_response(event)