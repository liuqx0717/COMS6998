import json
import requests
import boto3

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "POST"
}
ES_DOC_ENDPOINT = 'https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_doc/'
AUTH_ID = "3d5bba49-f5a7-ff72-99dc-3d1df442840a"
AUTH_TOKEN = "URrtLgIWuVqhZgFzuzyQ"


def lambda_handler(event, context):
    try:
        if event['resource'] == '/items':
            if event['httpMethod'] == 'POST':
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

                # extract seller info
                user_profile = {'id': id}
                for attr in response['UserAttributes']:
                    if attr['Name'] == 'custom:type' or attr['Name'] == 'custom:paypalUrl':
                        attr_name = attr['Name'].split(':')[-1]
                    elif attr['Name'] == 'phone_number':
                        attr_name = 'phone'
                    elif attr['Name'] == 'name':
                        attr_name = 'userName'
                    else:
                        attr_name = attr['Name']

                    user_profile[attr_name] = attr['Value']

                if 'type' not in user_profile:
                    return make_response(404, 'User type not defined')
                if user_profile['type'] != 'seller':
                    return make_response(403, 'Forbidden. Buyer has no access to post items')

                # extract item info
                item = event['item']
                item['seller'] = id
                item['sellerInfo'] = user_profile
                item['location'] = {}
                item['location']['lon'], item['location']['lat'], info = get_coordinate(user_profile['address'])

                # failed to get location
                if info:
                    return info

                header = {
                    "Content-Type": "application/json"
                }
                response = requests.post(url=ES_DOC_ENDPOINT, data=json.dumps(item), headers=header)
                if response.status_code != 201:
                    return make_response(response.status_code, response.reason)

                item_id = response.json()['_id']

                return make_response(200, item_id)

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /items')


def get_coordinate(address):
    street, city, state, postcode = address.split(',')

    url = "https://us-street.api.smartystreets.com/street-address?auth-id=" + AUTH_ID + "&auth-token=" + AUTH_TOKEN \
          + "&candidates=10&street=" + street + "&city=" + city + "&state=" + state + "&zipcode=" + postcode + "&match=invalid"

    url = url.replace(' ', "%20").replace('#', '%23')

    response = requests.get(url)

    if response.status_code != 200:
        return 181, 91, make_response(response.status_code, response.reason)

    add = response.json()[0]['metadata']

    return add['longitude'], add['latitude'], ''


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
