import json
import boto3
import time
import decimal
import random

OWNER_PHONE = '+19178680357'
OWNER_NAME = 'Julius'


# Process incoming kds data stream
def lambda_handler(event, context):
    face_id = event['faceID']
    image = event['img_address']

    temp_photo = boto3.resource('dynamodb').Table('smart_door_temp_photo')
    response = temp_photo.get_item(
        Key={
            'face_id': face_id
        }
    )

    # Discard duplicates
    if 'Item' in response and time.time() < response['Item']['ttl']:
        return {
            'status': False,
            'message': 'Duplicate requests'
        }

    temp_photo.put_item(
        Item={
            'face_id': face_id,
            'photo': image,
            'ttl': decimal.Decimal(time.time() + 300)
        }
    )

    visitor = boto3.resource('dynamodb').Table('smart_door_visitor')
    response = visitor.get_item(
        Key={
            'face_id': face_id
        }
    )

    # registered visitor
    if 'Item' in response:
        photo = response['Item']['photo']
        photo.append(image)
        visitor.update_item(
            Key={
                'face_id': face_id
            },
            UpdateExpression='SET photo = :val',
            ExpressionAttributeValues={
                ':val': photo
            }
        )
        generate_otp(face_id, response['Item']['name'], response['Item']['phone'])

        return {
            'status': True,
            'message': 'OTP generated'
        }

    # new visitor
    else:
        link = 'https://hw2.liuqx.net/add-visitor.html?id={}&photo={}'.format(face_id, image)
        text = 'Greetings {}, you have a new visitor at door. To grant access click {}'.format(OWNER_NAME, link)

        sns = boto3.client('sns')
        sns.publish(
            PhoneNumber=OWNER_PHONE,
            Message=text
        )

        return {
            'status': True,
            'message': 'Adding visitor prompted'
        }


# generate and send otp
def generate_otp(face_id, name, phone):
    otp = '{:06}'.format(random.randint(0, 999999))
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
