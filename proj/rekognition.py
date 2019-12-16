import boto3


def lambda_handler(event, context):
    name = event['imageName']

    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': 'mfl-pictures-bucket',
                'Name': name
            }
        },
        MaxLabels=10,
        MinConfidence=80)

    tags = [label['Name'].lower() for label in response['Labels']]

    return {
        'status': True,
        'tags': tags
    }
