# The following example creates a collection and displays its Amazon Resource Name (ARN).
#
# Change the value of collection_id to the name of collection you want to create.

import boto3

# AWS account info
ACCESS_KEY_ID = 'AKIAJCBNACHH3PPRVGXA'
SECRET_KEY = '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'
REGION = 'us-east-1'

def create_collection(collection_id):
    client = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_KEY, region_name=REGION)

    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')


def main():
    # Create a collection
    collection_id = 'Collection_test_0'
    create_collection(collection_id) # Collection ARN: aws:rekognition:us-east-1:685653151206:collection/Collection_test_0

if __name__ == "__main__":
    main()
