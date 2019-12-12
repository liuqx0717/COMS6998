import json
import string
import boto3

headers = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET,OPTIONS,PUT"
}


def lambda_handler(event, context):
    # print(json.dump(event))
    try:
        if event["resource"] == "/search":
            if event["httpMethod"] == "GET":
                # boto3.setup_default_session(region_name='us-east-1')
                # client = boto3.client('lambda')
                # response = client.invoke(
                #  FunctionName='arn:aws:lambda:us-east-1:831292248611:function:smart_door_fe_lf',
                #  Payload=json.dumps({'action':'authorize', 'otp':otp}).encode("utf-8"))
                # response_payload = json.loads(response["Payload"].read().decode("utf-8"))
                return {
                    "statusCode": 200,
                    "body": '{"results":[ {"url":"https://face-detect-6998.s3.amazonaws.com/10744586.jpg","labels":['
                            '"labels","labels"]}, {"url":"https://face-detect-6998.s3.amazonaws.com/73596321.jpg",'
                            '"labels":["labels","labels"]}, '
                            '{"url":"https://face-detect-6998.s3.amazonaws.com/99778582.jpg","labels":["labels",'
                            '"labels"]} ]})',
                    "headers": headers
                }
                # print(response_payload)
                return make_response(200, {"name": response_payload["name"]})

        # if resource/method not listed above
        return make_response(400, "Bad request.")


    except Exception as err:
        print(err)
        return make_response(500, "Internal error - hw2-apihandlerapi.")


# examples:
#     code=200, body={"content": "hello!"}
#     code=400, body={"Invalid input."}
def make_response(code, body):
    return {
        "statusCode": code,
        "body": json.dumps(body),
        "headers": headers
    }
