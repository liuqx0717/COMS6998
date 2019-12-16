import json
import requests
import boto3

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "GET, PUT"
}
ES_DOC_ENDPOINT = 'https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_doc/'


def lambda_handler(event, context):
    try:
        if event['resource'] == '/items/{id}':
            if event['httpMethod'] == 'GET':
                item_id = event['pathParameters']['id']

                response = requests.get(ES_DOC_ENDPOINT + item_id)
                if response.status_code != 200:
                    return make_response(response.status_code, response.reason)

                item = response.json()['_source']
                item['id'] = response.json()['_id']

                return make_response(200, item)

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

                item_id = event['pathParameters']['id']
                item_info = json.loads(event['body'])

                response = requests.get(ES_DOC_ENDPOINT + item_id)
                if response.status_code != 200:
                    return make_response(response.status_code, response.reason)

                item = response.json()['_source']

                if id != item['sellerId']:
                    return make_response(403, 'Forbidden. Only item owner can update item info')

                body = {'doc': item_info}
                url = ES_DOC_ENDPOINT + item_id + '/_update'
                header = {
                    "Content-Type": "application/json"
                }

                response = requests.post(url, data=json.dumps(body), headers=header)
                if response.status_code != 200:
                    return make_response(response.status_code, response.reason)

                return make_response(200, 'Update item info successful')

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /items/{id}')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
