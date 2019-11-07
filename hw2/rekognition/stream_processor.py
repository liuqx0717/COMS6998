# The following example creates a collection and displays its Amazon Resource Name (ARN).
#
# Change the value of collection_id to the name of collection you want to create.

import boto3
import json

# AWS account info
ACCESS_KEY_ID = 'AKIAJCBNACHH3PPRVGXA'
SECRET_KEY = 'qreGxTGSsrPL0jtckBLum4t00M08u2qeN7msiCEl'
REGION = 'us-east-1'

ArnVideoStream = 'arn:aws:kinesisvideo:us-east-1:685653151206:stream/ExampleStream/1573080662669'
ArnDataStream = 'arn:aws:kinesis:us-east-1:685653151206:stream/ExampleDataStream'
FaceMatchThreshold = 95
collection_id = 'Collection_test_0'
RoleArn = 'arn:aws:iam::685653151206:role/AmazonRekognitionServiceRole'

def create_stream_processor():
    client = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_KEY, region_name=REGION)

    print('Creating stream processor...')
    response = client.create_stream_processor(
        Input={
            'KinesisVideoStream': {
                'Arn': ArnVideoStream
            }
        },
        Output={
            'KinesisDataStream': {
                'Arn': ArnDataStream
            }
        },
        Name='ExampleStreamProcessor',
        Settings={
            'FaceSearch': {
                'CollectionId': collection_id,
                'FaceMatchThreshold': FaceMatchThreshold
            }
        },
        RoleArn = RoleArn
    )
    # print(json.dumps(response))
    print('Stream Processor ARN: ' + response['StreamProcessorArn'])
    # print('Status code: ' + str(response['StatusCode']))
    print('Done.')


def main():
    # Create a stream processor
    create_stream_processor() # "StreamProcessorArn": "arn:aws:rekognition:us-east-1:685653151206:streamprocessor/ExampleStreamProcessor"


if __name__ == "__main__":
    main()
