import json
import string
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

headers = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET,OPTIONS,PUT"
}


# examples:
#     code=200, body={"content": "hello!"}
#     code=400, body={"Invalid input."}
def make_response(code, body):
    return {
        "statusCode": code,
        "body": json.dumps(body),
        "headers": headers
    }


def lex(message):
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

    response = es.search(index="photos", body=query_body)
    print(type(response))
    print(response)
    # TODO: search result processing

    return response


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))

    try:
        if event["resource"] == "/search":
            if event["httpMethod"] == "GET":
                query = event['queryStringParameters']['q']
                lex_res = lex(query)
                print(lex_res)
                if not lex_res['status']:
                    return make_response(200, "Lex doesn't understand your words.")


                # This is a test return.
                return {
                    "statusCode": 200,
                    "body": '{"results":[ {"url":"https://face-detect-6998.s3.amazonaws.com/10744586.jpg","labels":['
                            '"labels","labels"]}, {"url":"https://face-detect-6998.s3.amazonaws.com/73596321.jpg",'
                            '"labels":["labels","labels"]}, '
                            '{"url":"https://face-detect-6998.s3.amazonaws.com/99778582.jpg","labels":["labels",'
                            '"labels"]} ]}',
                    "headers": headers
                }

        # if resource/method not listed above
        return make_response(400, "Bad request.")

    except Exception as err:
        print(err)
        return make_response(500, "Internal error - hw3.search-photos.py")
