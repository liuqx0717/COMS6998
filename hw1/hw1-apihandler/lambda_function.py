import json
import string
import random
import boto3

headers = {
    "access-control-allow-origin": "https://hw1.liuqx.net",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET,OPTIONS,POST"
}

def lambda_handler(event, context):
    # TODO implement

    #try:
        if event["resource"] == "/message":
            if event["httpMethod"] == "POST":
                #try:
                    bodyJson = event["body"]
                    body = json.loads(bodyJson)
                    msg = body["content"]
                    id = body["sessionid"]
                    
                    # TODO: invoke lex
                    boto3.setup_default_session(region_name='us-east-1')
                    client = boto3.client('lambda')
                    response = client.invoke(
                        FunctionName='arn:aws:lambda:us-east-1:530060456874:function:LF0',
                        Payload=json.dumps({'query':msg, 'userId': id}).encode("utf-8")
                    )
                    
                    response_payload = json.loads(response["Payload"].read().decode("utf-8"))
                    
                    print(response_payload)
                    
                    return make_response(
                        200, 
                        {
                            "sessionid": id,
                            "content": response_payload["content"]
                        }
                    )

                #except Exception as err:
                    return make_response(405, "Invalid input: " + bodyJson)

        if event["resource"] == "/session":
            if event["httpMethod"] == "GET":
                try:
                    sessionid = random_generator()
                    return make_response(200, {"sessionid": sessionid})

                except Exception as err:
                    return make_response(503, "Service unavailable.")


        # if resource/method not listed above
        return make_response(400, "Bad request.")

    #except:
        return make_response(500, "Internal error - hw1-apihandlerapi.")




# return value: string
def random_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


# examples:
#     code=200, body={"content": "hello!"}
#     code=400, body={"Invalid input."}
def make_response(code, body):
    return {
        "statusCode": code,
        "body": json.dumps(body),
        "headers": headers
    }