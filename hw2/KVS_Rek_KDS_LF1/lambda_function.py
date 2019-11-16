import json
import numpy as np
import base64
import random
import boto3
import cv2


def lambda_handler(event, context):
    # This part is used to get the endpoint
    kinesis_client = boto3.client('kinesisvideo')
    endpoint_response = kinesis_client.get_data_endpoint(
        StreamARN='arn:aws:kinesisvideo:us-east-1:530060456874:stream/ExampleStream/1573078203070',
        APIName='GET_MEDIA'
    )
    DataEndpoint = endpoint_response['DataEndpoint']
    print(DataEndpoint)

    # Get_media API
    video_client = boto3.client('kinesis-video-media', endpoint_url=DataEndpoint)
    stream_response = video_client.get_media(
        StreamARN='arn:aws:kinesisvideo:us-east-1:530060456874:stream/ExampleStream/1573078203070',
        StartSelector={
            'StartSelectorType': 'NOW'
        }
    )
    video_stream = stream_response['Payload'].read()
    # can use ['Payload'].read(1024 * 16384) reads min(16MB of payload, payload size)

    # Use openCV to get a frame from video_stream
    image_name = ""
    img_address = ""
    bucket = 'face-detect-6998'
    with open('/tmp/stream.mkv', 'wb') as f:
        f.write(video_stream)
        cap = cv2.VideoCapture('/tmp/stream.mkv')
        ret, frame = cap.read()
        if ret and np.shape(frame) != ():
            random.seed()
            image_name = str(random.randint(10000000, 99999999)) + '.jpg'
            cv2.imwrite('/tmp/' + image_name, frame)

            # save it into the S3 bucket
            s3_client = boto3.client('s3')
            s3_client.upload_file('/tmp/' + image_name, bucket, image_name)
            img_address = 'https://{}.s3.amazonaws.com/{}'.format(bucket, image_name)
            print(img_address)
            print('Image uploaded')
        cap.release()

    # read the data from KDS
    rekognition_client = boto3.client('rekognition')
    records = event['Records']
    faceID = ""
    for record in records:
        load = base64.b64decode(record['kinesis']['data'])
        payload = json.loads(load)
        FaceSearchResponses = payload["FaceSearchResponse"]
        for FaceSearchResponse in FaceSearchResponses:
            matched_faces = FaceSearchResponse["MatchedFaces"]
            # Get faceID. If no match, use Indexed Face. Else, parse event info
            if len(matched_faces) == 0 and image_name != "":
                index_response = rekognition_client.index_faces(
                    CollectionId='Face',
                    Image={
                        'S3Object': {
                            'Bucket': bucket,
                            'Name': image_name
                        }
                    },
                )
                faceID = index_response["FaceRecords"][0]["Face"]["FaceId"]
                print("************This is Indexed face***********", faceID)
            elif len(matched_faces) != 0:
                faceID = matched_faces[0]["Face"]["FaceId"]
                print("************This is matched face***********", faceID)

    """
    Todo
    I provide three parameters:
        img_address     Like    https://face-detect-6998.s3.amazonaws.com/28150579.jpg
                        if == "" means I get a empty frame. Just skip it
        image_name      Like    28150579.jpg
                        if == "" means I get a empty frame. Just skip it
        faceID          Like    ab4fc56d-e7c0-4502-907c-69a0435dc5c3
                        if == "" means I get a empty frame. Just skip it
    ONLY if img_address != NULL and faceID != NULL can we do following operation.
    """
    # send img_address and faceID for following process
    if img_address != "" and faceID != "":
        lambda_client = boto3.client("lambda")
        lambda_response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:831292248611:function:smart_door_kds_lf',
            Payload=json.dumps({"img_address": img_address, "faceID": faceID})
        )
        print(lambda_response)

    return{
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
