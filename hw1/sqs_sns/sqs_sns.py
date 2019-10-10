import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    sqs = boto3.client(
        'sqs',
        aws_access_key_id='AKIA4DDHBCIR6VG2IC7Y',
        aws_secret_access_key='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'
        )
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/831292248611/dining_concierge',
        MaxNumberOfMessages=1
        )
    
    order = json.loads(response.get('Messages')[0]['Body'])
        
    try:
        if event["httpMethod"] == "POST":
            try:
                cuisine = order["cuisine"]

                # TODO: invoke elasiticsearch
                boto3.setup_default_session(region_name='us-east-2')
                client = boto3.client('lambda')
                response = client.invoke(
                    FunctionName='arn:aws:lambda:us-east-2:685653151206:function:LF_db',
                    Payload=json.dumps({'categories':cuisine}).encode("utf-8")
                )
                
                response_payload = json.loads(response["Payload"].read().decode("utf-8"))
                
                #print(response_payload)
                
                restaurant = response_payload['body']['Item']

            except Exception as err:
                print(err)
                return {
                    'statusCode': 405, 
                    'body': "Invalid input: " + json.dumps(cuisine),
                    'err': str(err)
                }
        
        else:
            # if method not listed above
            return {
                'statusCode': 400, 
                'body': "Bad request."
            }

    except Exception as err:
        return {
            'statusCode': 500, 
            'body': "Internal error - dining_concierge_lf2.",
            'err': str(err)
        }
        
    boto3.setup_default_session(region_name='us-east-1')
    sns = boto3.client(
        'sns',
        aws_access_key_id='AKIA4DDHBCIR36TEDGGA',
        aws_secret_access_key='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'
        )

    text = """Hello! Here are my {} restaurant suggestions for {} people, 
    for {} at {}: {}, located at {}. Enjoy your meal!""".format(
        order['cuisine'], order['numberOfPeople'], order['diningDate'], 
        order['diningTime'], restaurant['name']['S'], restaurant['address']['S']
        )
    
    response = sns.publish(
        PhoneNumber=order['phoneNumber'],
        Message=text
        )
    
    return response
