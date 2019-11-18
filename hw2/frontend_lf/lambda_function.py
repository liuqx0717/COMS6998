import json
import boto3
from boto3.dynamodb.conditions import Key
import time
import random
import decimal


def lambda_handler(event, context):
    if event['action'] == 'authorize':
        return authorize(event['otp'])

    elif event['action'] == 'add':
        return add(event['id'], event['name'], event['phoneNumber'])


# Verify OTP for guest access
def authorize(otp):
    authorized = False
    name = ''

    passcode = boto3.resource('dynamodb').Table('smart_door_passcode')
    response = passcode.query(
        IndexName='otp-index',
        KeyConditionExpression=Key('otp').eq(otp)
    )

    if len(response['Items']) > 0:
        face_id = response['Items'][0]['face_id']
        ttl = response['Items'][0]['ttl']
        if time.time() <= ttl:
            authorized = True

    # Delete password and retrieve visitor info
    if authorized:
        passcode.delete_item(
            Key={
                'face_id': face_id
            }
        )

        visitor = boto3.resource('dynamodb').Table('smart_door_visitor')
        response = visitor.get_item(
            Key={
                'face_id': face_id
            }
        )
        name = response['Item']['name']

        temp_photo = boto3.resource('dynamodb').Table('smart_door_temp_photo')
        temp_photo.delete_item(
            Key={
                'face_id': face_id
            }
        )

    return {
        'authorized': authorized,
        'name': name
    }


# Register visitor
def add(face_id, name, phone):
    status = False

    # retrieve temp photos for first-time visitor
    temp_photo = boto3.resource('dynamodb').Table('smart_door_temp_photo')
    response = temp_photo.get_item(
        Key={
            'face_id': face_id
        }
    )

    photo = []
    if 'Item' in response:
        photo.append(response['Item']['photo'])

    visitor = boto3.resource('dynamodb').Table('smart_door_visitor')
    visitor.put_item(
        Item={
            'face_id': face_id,
            'name': name,
            'phone': phone,
            'photo': photo
        }
    )

    time.sleep(1)
    response = visitor.get_item(
        Key={
            'face_id': face_id
        }
    )

    if 'Item' in response:
        status = True
        message = 'Register succeed'
    else:
        message = 'Register failed'

    if status:
        generate_otp(face_id, name, phone)

    return {
        'status': status,
        'message': message
    }


def generate_otp(face_id, name, phone):
    # six digit otp
    otp = '{:06}'.format(random.randint(0, 999999))
    # expire in 5 mins
    ttl = decimal.Decimal(time.time() + 300)

    passcode = boto3.resource('dynamodb').Table('smart_door_passcode')
    passcode.put_item(
        Item={
            'face_id': face_id,
            'otp': otp,
            'ttl': ttl
        }
    )

    text = 'Greetings, {}. Your one-time password is {}, valid for 5 minutes.'.format(name, otp)

    sns = boto3.client('sns')
    sns.publish(
        PhoneNumber=phone,
        Message=text
    )
