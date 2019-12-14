import boto3
import json
from boto3.dynamodb.conditions import Key

CLIENT_ID = '2a2sr0e7ktos7b3l1r13tlq0g8'
HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET"
}


def lambda_handler(event, context):
    try:
        if event['resource'] == '/orders':
            if event['httpMethod'] == 'GET':
                access_token = event['pathParameters']['accessToken']

                cognito = boto3.client('cognito-idp')
                response = cognito.get_user(
                    AccessToken=access_token
                )

                id = response['Username']
                if not id:
                    return make_response(404, 'User does not exist')

                type = ''
                for attr in response['UserAttributes']:
                    if attr['Name'] == 'custom:type':
                        type = attr['Value']
                if type == 'seller':
                    idx = 'seller-index'
                elif type == 'buyer':
                    idx = 'buyer-index'
                else:
                    return make_response(404, 'User type not defined')

                orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                response = orders_table.query(
                    IndexName=idx,
                    KeyConditionExpression=Key(type).eq(id),
                    FilterExpression=Key('status').eq('finished')
                )

                return make_response(200, response['Items'])

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /orders')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'header': HEADERS
    }

