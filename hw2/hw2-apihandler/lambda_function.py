import json
import string
import boto3

headers = {
  "access-control-allow-origin": "*",
  "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
  "access-control-allow-methods": "GET,OPTIONS,PUT"
}

def lambda_handler(event, context):
  #print(json.dump(event))
  #return make_response(200, "Hello!!!")
  try:
    if event["resource"] == "/authorize/{otp}":
      if event["httpMethod"] == "GET":
        otp = event["pathParameters"]["otp"]
          
        # TODO
        #boto3.setup_default_session(region_name='us-east-1')
        #client = boto3.client('lambda')
        #response = client.invoke(
        #  FunctionName='arn:aws:lambda:us-east-1:530060456874:function:LF0',
        #  Payload=json.dumps({'query':msg, 'userId': id}).encode("utf-8")
        #)
        #
        #response_payload = json.loads(response["Payload"].read().decode("utf-8"))
          
        #print(response_payload)

        if otp == "lqx":
          return make_response(200, {"name": "liuqx"})
        else:
          return make_response(403, "Permission denied. ")

    elif event["resource"] == "/visitors/{id}":
      if event["httpMethod"] == "PUT":
        try:
          id = event["pathParameters"]["id"]
          bodyJson = event["body"]
          body = json.loads(bodyJson)
          name = body["name"]
          phoneNumber = body["phoneNumber"]
        except:
          return make_response(400, "Invalid input: " + bodyJson)
        # TODO

        if id == "lqx":
          return make_response(200, "OK: " + name + ", " + phoneNumber + ".")
        else:
          return make_response(404, "The id does not exist.")
        



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



