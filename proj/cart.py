import boto3
import json
from boto3.dynamodb.conditions import Key
import requests
import uuid
import time

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "GET, PUT, POST, DELETE"
}
ES_DOC_ENDPOINT = 'https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_doc/'


def lambda_handler(event, context):
    try:
        if event['resource'] == '/cart':
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
                    return make_response(403, 'Forbidden. Seller has no access to carts')
                elif not user_type:
                    return make_response(404, 'User type not defined')

                orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                response = orders_table.query(
                    IndexName='buyer-index',
                    KeyConditionExpression=Key('buyer').eq(id),
                    FilterExpression=Key('stat').eq('wishlist')
                )

                orders = []
                for order in response['Items']:
                    updated_order = update_order(order, orders_table)
                    orders.append(updated_order)

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

                return make_response(200, orders)

            if event['httpMethod'] == 'PUT':
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

                item_id = event['queryStringParameters']['item']

                response = requests.get(url=ES_DOC_ENDPOINT + item_id)
                if response.status_code != 200:
                    return make_response(response.status_code, response.reason)

                item = response.json()['_source']
                if not item['available']:
                    return make_response(404, 'Item unavailable')
                if item['stock'] < 1:
                    return make_response(404, 'Item out of stock')

                orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                response = orders_table.query(
                    IndexName='buyer-index',
                    KeyConditionExpression=Key('buyer').eq(id),
                    FilterExpression=Key('seller').eq(item['sellerId']) & Key('stat').eq('wishlist')
                )

                # create new wishlist
                if not response['Items']:
                    orders_table.put_item(
                        Item={
                            'id': str(uuid.uuid4()),
                            'itms': [item_id],
                            'buyer': id,
                            'seller': item['sellerId'],
                            'sellerInfo': item['sellerInfo'],
                            'price': str(item['price']),
                            'prvPrice': str(item['prvPrice']),
                            'stat': 'wishlist'
                        }
                    )
                # append current wishlist
                else:
                    order = response['Items'][0]
                    order['itms'].append(item_id)
                    updated_order = update_order(order, orders_table)

                return make_response(200, 'Adding to cart successful')

            if event['httpMethod'] == 'POST':
                order_id = event['queryStringParameters']['order']

                orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                response = orders_table.get_item(
                    Key={
                        'id': order_id
                    }
                )
                if 'Item' not in response:
                    return make_response(404, 'Order does not exist')
                order = response['Item']

                order = update_order(order, orders_table)
                order['stat'] = 'finished'
                order['finishTime'] = str(time.time())
                orders_table.update_item(
                    Key={
                        'id': order['id']
                    },
                    UpdateExpression='SET stat = :val1, finishTime = :val2',
                    ExpressionAttributeValues={
                        ':val1': order['stat'],
                        ':val2': order['finishTime']
                    }
                )

                adjust_stock(order)

                return make_response(200, order['sellerInfo']['paypalUrl'])

            if event['httpMethod'] == 'DELETE':
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

                items = eval(event['queryStringParameters']['items'])

                for item_id in items:
                    response = requests.get(url=ES_DOC_ENDPOINT + item_id)
                    if response.status_code != 200:
                        return make_response(response.status_code, response.reason)

                    item = response.json()['_source']

                    orders_table = boto3.resource('dynamodb').Table('mfl_orders')
                    response = orders_table.query(
                        IndexName='buyer-index',
                        KeyConditionExpression=Key('buyer').eq(id),
                        FilterExpression=Key('seller').eq(item['sellerId']) & Key('stat').eq('wishlist')
                    )
                    order = response['Items'][0]

                    # keep order
                    if len(order['itms']) > 1:
                        new_items = order['itms']
                        new_items.remove(item_id)
                        orders_table.update_item(
                            Key={
                                'id': order['id']
                            },
                            UpdateExpression='SET itms = :val',
                            ExpressionAttributeValues={
                                ':val': new_items
                            }
                        )
                        update_order(order, orders_table)
                    # remove order
                    else:
                        orders_table.delete_item(
                            Key={
                                'id': order['id']
                            }
                        )

                    return make_response(200, 'Remove items successful')

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /cart')


def update_order(order, orders_table):
    price, prvPrice = 0, 0
    temp_items = []

    for item_id in order['itms']:
        response = requests.get(url=ES_DOC_ENDPOINT + item_id)
        if response.status_code != 200:
            continue
        temp_items.append(item_id)

        item = response.json()['_source']
        if not (item['available'] or item['stock'] < 1):
            continue

        price += item['price']
        prvPrice += item['prvPrice']

    if price != float(order['price']) or prvPrice != float(order['prvPrice']) or temp_items != order['itms']:
        orders_table.update_item(
            Key={
                'id': order['id']
            },
            UpdateExpression='SET itms = :val1, price = :val2, prvPrice = :val3',
            ExpressionAttributeValues={
                ':val1': temp_items,
                ':val2': str(price),
                ':val3': str(prvPrice)
            }
        )

    return order


def adjust_stock(order):
    for item in order['itms']:
        response = requests.get(url=ES_DOC_ENDPOINT + item)
        if response.status_code != 200:
            continue
        stock = response.json()['_source']['stock']

        body = {
            'doc': {
                'stock': stock - 1
            }
        }
        url = ES_DOC_ENDPOINT + item + '/_update'
        header = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(body), headers=header)


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
