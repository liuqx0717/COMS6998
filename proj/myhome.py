import boto3
import json

CLIENT_ID = '2a2sr0e7ktos7b3l1r13tlq0g8'
HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET, PUT"
}


def lambda_handler(event, context):
    try:
        if event['resource'] == '/myhome':
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
                    return make_response(204, {})

                return make_response(200, user_profile)

            if event['httpMethod'] == 'PUT':
                if 'Access-Token' in event['headers']:
                    access_token = event['headers']['Access-Token']
                elif 'access-token' in event['headers']:
                    access_token = event['headers']['access-token']
                else:
                    return make_response(400, 'Empty access token')

                try:
                    body = json.loads(event['body'])
                except:
                    return make_response(405, 'Invalid input' + event['body'])

                user_attributes = []
                for attr in body:
                    if attr == 'type' or attr == 'paypalUrl':
                        attr_name = 'custom:' + attr
                    elif attr == 'userName':
                        attr_name = 'name'
                    elif attr == 'phone':
                        attr_name = 'phone_number'
                    elif attr == 'email' or attr == 'address':
                        attr_name = attr
                    else:
                        return make_response(405, 'Illegal field name: ' + attr)

                    user_attributes.append(
                        {'Name': attr_name, 'Value': body[attr]}
                    )

                cognito = boto3.client('cognito-idp')
                response = cognito.update_user_attributes(
                    UserAttributes=user_attributes,
                    AccessToken=access_token
                )

                return make_response(200, 'Update information successful')

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /myhome')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
