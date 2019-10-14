import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/831292248611/dining_concierge',
        MaxNumberOfMessages=1
        )
    
    try:
        receiptHandler = response['Messages'][0]['ReceiptHandle']
        order = json.loads(response['Messages'][0]['Body'])
    except Exception as err:
        return {
            'statusCode': 400, 
            'body': 'Bad request when retrieving messgaes from SQS',
            'err': str(err)
        }
        
    response = sqs.delete_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/831292248611/dining_concierge',
        ReceiptHandle=receiptHandler
        )
    
    cuisine = order['cuisine'].lower()
    if cuisine not in ['chinese', 'american', 'mexican', 'italian', 'japanese']:
        return {
            'statusCode': 405,
            'body': 'Invalid input: {}'.format(order['cuisine'])
        }

    # TODO: invoke elasiticsearch
    boto3.setup_default_session(region_name='us-east-2')
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName='arn:aws:lambda:us-east-2:685653151206:function:LF_db',
        Payload=json.dumps({'cuisine':cuisine}).encode("utf-8")
    )
        
    try:
        response_payload = json.loads(response["Payload"].read().decode("utf-8"))
    except Exception as err:
        return {
            'statusCode': 400, 
            'body': 'Bad request when retrieving messgaes from ElasticSearch',
            'err': str(err)
        }
    
    restaurant = response_payload

    boto3.setup_default_session(region_name='us-east-1')
    sns = boto3.client('sns')

    text = '''Hello! Here are my {} restaurant suggestions for {} people, for {} at {}: {}, located at {}. Enjoy your meal!'''.format(
        order['cuisine'].lower(), order['numberOfPeople'], order['diningDate'], 
        order['diningTime'], restaurant['name']['S'], restaurant['address']['S']
        )
    
    response = sns.publish(
        PhoneNumber=order['phoneNumber'],
        Message=text
        )
    
    return response
