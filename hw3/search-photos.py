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
    string = ""
    for keyword in keywords:
        string += str(keyword + " ")

    print("string = ", string)

    query_body = {
        "query": {
            "match": {"labels": string}
        }
    }

    response = es.search(index="photos", body=query_body)  # type: dict
    print(response)
    # TODO: search result processing

    return response


def lex_search(message):
    lf = boto3.client('lambda')
    response = lf.invoke(
        FunctionName='arn:aws:lambda:us-east-1:831292248611:function:photo_album_lex_lf',
        Payload=json.dumps({'message': message}).encode("utf-8")
    )
    # print("response = ", json.dumps(json.loads(str(response)), indent=4))
    print("type = ", type(response), "\nlex_response = ", response)
    response_payload = json.loads(response["Payload"].read().decode("utf-8"))

    if response_payload['status'] is False:
        res = {
            "status": False
        }
        return res

    else:
        keywords = response_payload['keywords']  # type: list
        print("keywords = ", keywords)
        result = search(keywords)
        res = {
            "status": True,
            "result": result
        }
        return res


def lambda_handler(event, context):
    print(json.dumps(event, indent=4))

    try:
        if event["resource"] == "/search":
            if event["httpMethod"] == "GET":
                query = event['queryStringParameters']['q']
                print("query = ", query)
                lex_search_res = lex_search(query)
                print("lex_search_res = ", json.dumps(lex_search_res, indent=4))
                if not lex_search_res['status']:
                    print("\nLex doesn't understand.")
                    return make_response(200, "Lex doesn't understand your words.")
                else:
                    if lex_search_res['result']['hits']['total']['value'] == 0:
                        print("\nNo matches.")
                        return make_response(200, "No matches.")
                    else:
                        results = []
                        for hit in lex_search_res['result']['hits']['hits']:
                            url = str("https://" + hit['_source']['bucket'] + ".s3.amazonaws.com/" + hit['_source'][
                                'objectKey'])
                            result = {"url": url}
                            results.append(result)
                        body = {"results": results}
                        body = json.dumps(body)
                        # print(json.dumps(body, indent=4))
                        print("body = ", body)
                        return {
                            "statusCode": 200,
                            "body": body,
                            "headers": headers
                        }

                # # This is a test return.
                # # body = '{"results":[ \
                # # {"url":"https://face-detect-6998.s3.amazonaws.com/10744586.jpg","labels":["labels","labels"]}, \
                # # {"url":"https://face-detect-6998.s3.amazonaws.com/73596321.jpg","labels":["labels","labels"]}, \
                # # {"url":"https://face-detect-6998.s3.amazonaws.com/99778582.jpg","labels":["labels","labels"]}]}'
                # body = '{"results":[ \
                # {"url":"https://face-detect-6998.s3.amazonaws.com/10744586.jpg"}, \
                # {"url":"https://face-detect-6998.s3.amazonaws.com/73596321.jpg"}, \
                # {"url":"https://face-detect-6998.s3.amazonaws.com/99778582.jpg"}]}'
                # print("body = ", json.dumps(json.loads(body), indent=4))
                # return {
                #     "statusCode": 200,
                #     "body": body,
                #     "headers": headers
                # }

        # if resource/method not listed above
        return make_response(400, "Bad request.")

    except Exception as err:
        print(err)
        return make_response(500, "Internal error - hw3.search-photos.py")

# non-hit result:
#  "result": {
#         "took": 6,
#         "timed_out": false,
#         "_shards": {
#             "total": 5,
#             "successful": 5,
#             "skipped": 0,
#             "failed": 0
#         },
#         "hits": {
#             "total": {
#                 "value": 0,
#                 "relation": "eq"
#             },
#             "max_score": null,
#             "hits": []
#         }
#     }


# Hit result:
# "result": {
#     "took": 4,
#     "timed_out": false,
#     "_shards": {
#         "total": 5,
#         "successful": 5,
#         "skipped": 0,
#         "failed": 0
#     },
#     "hits": {
#         "total": {
#             "value": 3,
#             "relation": "eq"
#         },
#         "max_score": 1.2199391,
#         "hits": [
#             {
#                 "_index": "photos",
#                 "_type": "_doc",
#                 "_id": "02c64477-bd55-43f1-88d3-b6c113904f77",
#                 "_score": 1.2199391,
#                 "_source": {
#                     "objectKey": "plant-based-milk.jpg",
#                     "bucket": "photobucket0",
#                     "createdTimestamp": "2019-12-07 00:26:03.702685",
#                     "labels": [
#                         "beverage",
#                         "drink",
#                         "milk",
#                         "plant",
#                         "vegetable",
#                         "nut",
#                         "food",
#                         "almond"
#                     ]
#                 }
#             },
#             {
#                 "_index": "photos",
#                 "_type": "_doc",
#                 "_id": "3adc60e3-7291-49fc-955b-14bbd7aa5bac",
#                 "_score": 1.0378369,
#                 "_source": {
#                     "objectKey": "plant-based-milk.jpg",
#                     "bucket": "photobucket0",
#                     "createdTimestamp": "2019-12-07 00:28:41.387028",
#                     "labels": [
#                         "drink",
#                         "milk",
#                         "beverage",
#                         "plant",
#                         "food",
#                         "nut",
#                         "vegetable",
#                         "almond"
#                     ]
#                 }
#             },
#             {
#                 "_index": "photos",
#                 "_type": "_doc",
#                 "_id": "9b9b6509-bdbd-4f9f-913c-6a6ccbd5d39c",
#                 "_score": 0.86312973,
#                 "_source": {
#                     "objectKey": "plant-based-milk.jpg",
#                     "bucket": "photobucket0",
#                     "createdTimestamp": "2019-12-12 18:56:49.000993",
#                     "labels": [
#                         "milk",
#                         "drink",
#                         "beverage",
#                         "plant",
#                         "vegetable",
#                         "food",
#                         "nut",
#                         "almond"
#                     ]
#                 }
#             }
#         ]
#     }
# }