import boto3
import json
from boto3.dynamodb.conditions import Key
import time

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "GET"
}


def lambda_handler(event, context):
    try:
        if event['resource'] == '/orders':
            if event['httpMethod'] == 'GET':
                if 'Access-Token' in event['headers']:
                    access_token = event['headers']['Access-Token']
                elif 'access-token' in event['headers']:
                    access_token = event['headers']['access-token']
                else:
                    return make_response(400, 'Empty access token')

                cognito = boto3.client('cognito-idp')
                response = cognito.get_user(
                    AccessToken=access_token
                )

                id = response['Username']
                if not id:
                    return make_response(404, 'User does not exist')

                user_type = ''
                for attr in response['UserAttributes']:
                    if attr['Name'] == 'custom:type':
                        user_type = attr['Value']
                if user_type == 'seller':
                    idx = 'seller-index'
                elif user_type == 'buyer':
                    idx = 'buyer-index'
                else:
                    return make_response(404, 'User type not defined')

                orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                response = orders_table.query(
                    IndexName=idx,
                    KeyConditionExpression=Key(user_type).eq(id),
                    FilterExpression=Key('stat').eq('finished')
                )

                orders = response['Items']
                for order in orders:
                    for attr in order:
                        if attr == 'finishTime':
                            order[attr] = time.ctime(float(order[attr]))
                        if attr == 'price' or attr == 'prvPrice':
                            order[attr] = float(order[attr])
                    order['items'] = order['itms']
                    order['status'] = order['stat']
                    del order['itms']
                    del order['stat']
                orders = sorted(orders, key=lambda val: val['finishTime'], reverse=True)

                return make_response(200, orders)

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /orders')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
