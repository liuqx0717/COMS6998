# This example displays the face identifiers for faces added to the collection.
#
# Change the value of collectionId to the name of the collection that you want to add a face to.
# Replace the values of bucket and photo with the names of the Amazon S3 bucket and image that you used in step 2.
# The MaxFaces input parameter restricts the number of indexed faces to 1. Remove or change its value to suit your
# needs.


import boto3

# AWS account info
ACCESS_KEY_ID = 'AKIAJCBNACHH3PPRVGXA'
SECRET_KEY = 'qreGxTGSsrPL0jtckBLum4t00M08u2qeN7msiCEl'
REGION = 'us-east-1'


def add_faces_to_collection(bucket, photo, collection_id):
    client = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_KEY, region_name=REGION)

    response = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])

    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])


def main():
    # Add faces
    bucket = 'photobucket0'
    collection_id = 'Collection_test_0'
    photo = 'hebe1_copy.jpeg'

    indexed_faces_count = add_faces_to_collection(bucket, photo, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))


if __name__ == "__main__":
    main()

# Results for hebe1.jpeg
# Faces indexed:
#   Face ID: 9af68537-d09a-405f-9602-2f07dd759c6c
#   Location: {'Width': 0.3961983621120453, 'Height': 0.5184130668640137, 'Left': 0.15073339641094208, 'Top': 0.16435293853282928}
#
# Results for hebe2.jpg
# Faces indexed:
#   Face ID: 345643ad-4128-4897-9691-e48faa628084
#
# Results for hebe1.jpeg
# Faces indexed:
#   Face ID: 9af68537-d09a-405f-9602-2f07dd759c6c
#
# Results for hebe1_copy.jpeg
# Faces indexed:
#   Face ID: f4918710-2a2c-4986-9054-785b4c67237c
