import boto3
import json
import uuid
import base64

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "POST, DELETE"
}


def lambda_handler(event, context):
    try:
        if event['resource'] == '/pictures':
            if event['httpMethod'] == 'POST':
                image = event['body']
                image_name = str(uuid.uuid4()) + '.jpg'
                image_path = '/tmp/' + image_name

                with open(image_path, 'wb') as f:
                    f.write(base64.b64decode(image))

                bucket = boto3.resource('s3').Bucket('mfl-pictures-bucket')
                bucket.upload_file(image_path, image_name)
                image_url = 'https://mfl-pictures-bucket.s3.amazonaws.com/{}'.format(image_name)

                return make_response(200, image_url)

            if event['httpMethod'] == 'DELETE':
                image_url = event['queryStringParameters']['url']
                image_name = image_url.split('/')[-1]

                bucket = boto3.resource('s3').Bucket('mfl-pictures-bucket')
                response = bucket.delete_objects(
                    Delete={
                        'Objects': [
                            {'Key': image_name}
                        ]
                    }
                )

                return make_response(200, 'Pictures deletion successful')

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /pictures')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
