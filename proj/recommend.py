import json
from botocore.vendored import requests

CLIENT_ID = '2a2sr0e7ktos7b3l1r13tlq0g8'
HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "GET"
}
ES_ENDPOINT = "https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_search"


def lambda_handler(event, context):
    lat = event['lat']
    lon = event['lon']

    query_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "available": 1
                    }
                },
                "should": [
                    {"match": {"title": ""}},
                    {"match": {"description": ""}},
                    {"match": {"category": ""}},
                    {"match": {"tag": ""}}
                ],
                "filter": [
                    {
                        "geo_distance": {
                            "distance": "5km",
                            "location": {
                                "lat": lat,
                                "lon": lon
                            }
                        }
                    }
                ]
            }
        }
    }

    header = {
        "Content-Type": "application/json"
    }
    response = requests.get(
        url=ES_ENDPOINT,
        data=json.dumps(query_body),
        headers=header).json()

    # Process search result.
    results = []
    if response['hits']['total']['value'] != 0:
        for hit in response['hits']['hits']:
            result = hit['_source']
            result['id'] = hit['_id']
            results.append(result)

    return make_response(200, results)


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
