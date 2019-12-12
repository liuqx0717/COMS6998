import json
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


def search(keywords):
    host = 'vpc-photos-rxqmfbkp3mzqjkteqaecvpkmtm.us-east-1.es.amazonaws.com'
    region = 'us-east-1'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    # TODO: input format of labels. 'keywords' is a list of keywords
    query_body = {
        "query": {
            "match": {"labels": str(keywords)}
        }
    }

    # TODO: search result processing
    return es.search(index="photos", body=query_body)


def lambda_handler(event, context):
    message = event['message']
    lf = boto3.client('lambda')

    response = lf.invoke(
        FunctionName='arn:aws:lambda:us-east-1:831292248611:function:photo_album_lex_lf',
        Payload=json.dumps({'message': message}).encode("utf-8")
    )
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))

    if response_payload['status'] is False:
        return {
            'status': False,
            'result': ''
        }

    keywords = response_payload['keywords']  # type list
    res = search(keywords)

    return {
        'status': True,
        'result': res
    }
