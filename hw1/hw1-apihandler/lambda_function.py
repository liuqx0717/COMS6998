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


headers = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET,OPTIONS,POST"
}

def lambda_handler(event, context):
    # TODO implement

    try:
        if event["resource"] == "/message":
            if event["httpMethod"] == "POST":
                try:
                    bodyJson = event["body"]
                    body = json.loads(bodyJson)
                    msg = body["content"]

                    
                    return make_response(200, {"content": msg})

                except Exception as err:
                    return make_response(405, "Invalid input: " + bodyJson)

        # if resource/method not listed above
        return make_response(400, "Bad request.")

    except:
        return make_response(500, "Internal error - hw1-apihandlerapi.")



# examples:
#     code=200, body={"content": "hello!"}
#     code=400, body={"Invalid input."}
def make_response(code, body):
    return {
        "statusCode": code,
        "body": json.dumps(body),
        "headers": headers
    }