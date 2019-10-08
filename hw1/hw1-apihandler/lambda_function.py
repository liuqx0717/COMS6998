import json
import boto3

def process_msg(text, id):
    client = boto3.client('lex-runtime', region_name='us-east-1',
                      aws_access_key_id='AKIAXW2QQWOVNDX6POUJ',
                      aws_secret_access_key='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')

    resp = client.post_content(
        botName='DiningBot',
        botAlias='DiningBotBETA',
        userId=userId,
        sessionAttributes={},
        contentType="text/plain; charset=utf-8",
        inputStream=query

    )

    return resp['ResponseMetadata']['HTTPHeaders']['x-amz-lex-message']



def lambda_handler(event, context):
    # TODO implement

    try:
        headers = {
            "access-control-allow-origin": "*",
            "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "access-control-allow-methods": "GET,OPTIONS,POST"
        }

        if event["resource"] == "/message":
            if event["httpMethod"] == "POST":
                try:
                    bodyJson = event["body"]
                    body = json.loads(bodyJson)
                    msg = body["content"]

                    
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "content": msg
                        }),
                        "headers": headers
                    }
                except Exception as err:
                    return {
                        "statusCode": 405,
                        "body": json.dumps("Invalid input: " + bodyJson),
                        "headers": headers
                    }

        # if resource/method not listed above
        return {
            "statusCode": 400,
            "body": json.dumps("Bad request."),
            "headers": headers
        }

    except:
        return {
            "statusCode": 500,
            "body": json.dumps("Internal error - hw1-apihandlerapi."),
            "headers": headers
        }
