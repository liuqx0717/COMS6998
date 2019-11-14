import boto3
import json


class rekognitionProcessObject:

    def __init__(self, kinesis_info):
        self._client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id='AKIAXW2QQWOVKRVDJX6F',
         aws_secret_access_key='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')
        self._kvsARN = kinesis_info['kvsARN']
        self._kdsARN = kinesis_info['kdsARN']
        self._roleARN = kinesis_info['roleARN']
        self._name = kinesis_info['processName']
        self._collectionID = kinesis_info['collectionID']

    def creat_collection(self):
        response = self._client.create_collection(
            CollectionId=self._collectionID
        )
        return response

    def show_collection(self):
        response = self._client.list_collections(
            # NextToken='string',
            # MaxResults=123
        )
        return response

    def delete_collection(self):
        response = self._client.delete_collection(
            CollectionId=self._collectionID
        )


    def create_processor(self):
        response = self._client.create_stream_processor(
            Input={
                'KinesisVideoStream': {
                    'Arn': self._kvsARN
                }
            },
            Output={
                'KinesisDataStream': {
                    'Arn': self._kdsARN
                }
            },
            Name=self._name,
            Settings={
                'FaceSearch': {
                    'CollectionId': self._collectionID,
                    'FaceMatchThreshold': 0.85
                }
            },
            RoleArn=self._roleARN
        )
        return response

    def start(self):
        response = self._client.start_stream_processor(
            Name=self._name
        )

    def stop(self):
        response = self._client.stop_stream_processor(
            Name=self._name
        )

    def delete(self):
        response = self._client.delete_stream_processor(
            Name=self._name
        )

    def show_process(self, MaxResults=100):
        response = self._client.list_stream_processors(
            # NextToken='string',
            MaxResults=MaxResults
        )
        return response

    def indexFace(self, bucket, name):
        response = self._client.index_faces(
            CollectionId=self._collectionID,
            Image={
                # 'Bytes': b'bytes',
                'S3Object': {
                    'Bucket': bucket,
                    'Name': name
                }
            }
        )
        return response["FaceRecords"][0]["Face"]["FaceId"]

    def show_collection(self):
        response = self._client.describe_collection(
            CollectionId=self._collectionID
        )
        return response

    def delete_face(self, FaceIds):
        response = self._client.delete_faces(
            CollectionId=self._collectionID,
            FaceIds=FaceIds
        )
        return response

    def show_faces(self):
        response = self._client.list_faces(
            CollectionId=self._collectionID
        )
        return response

kinesis_info = {
    "kvsARN" : "arn:aws:kinesisvideo:us-east-1:530060456874:stream/ExampleStream/1573078203070",
    "kdsARN" : "arn:aws:kinesis:us-east-1:530060456874:stream/AmazonRekognitionFaceDetect",
    "processName" : "FaceDetect",
    "roleARN" : "arn:aws:iam::530060456874:role/FaceDetect",
    "collectionID" : "Face"
}

Face_recognized = rekognitionProcessObject(kinesis_info)
# res3 = Face_recognized.creat_collection()
# print(res3)
res4 = Face_recognized.show_collection()
print(res4)
# res1 = Face_recognized.create_processor()
# print(res1)
# Face_recognized.start()
res2 = Face_recognized.show_process()
print(json.dumps(res2, indent=2))
# Face_recognized.stop()
# Face_recognized.delete()
# Face_recognized.delete_collection()
# res5 = Face_recognized.indexFace('face-detect-6998','13142040.jpg')
# print(json.dumps(res5, indent=2))
# "FaceId": "d8f2e3b9-1701-496d-9ba7-a520e5081d5b"
res6 = Face_recognized.show_collection()
print(res6)
# res7 = Face_recognized.delete_face(["ab4fc56d-e7c0-4502-907c-69a0435dc5c3", "e5c4b3fb-1140-4834-a650-3dc2ea40c4bb"])
# print(res7)
res8 = Face_recognized.show_collection()
print(res8)
res9 = Face_recognized.show_faces()
print(json.dumps(res9, indent=2))