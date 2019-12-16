import json
import requests

HEADERS = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Access-Token",
    "access-control-allow-methods": "GET"
}
ES_SEARCH_ENDPOINT = "https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_search"


def lambda_handler(event, context):
    try:
        if event['resource'] == '/recommendation':
            if event['httpMethod'] == 'GET':
                lat = event['queryStringParameters']['lat']
                lon = event['queryStringParameters']['lon']

                query_body = {
                    "query": {
                        "bool": {
                            "must": {
                                "match": {
                                    "available": 1
                                }
                            },
                            "filter": [
                                {
                                    "geo_distance": {
                                        "distance": "10km",
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
                    url=ES_SEARCH_ENDPOINT,
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

        return make_response(400, 'Bad requests')

    except Exception as err:
        print(err)
        return make_response(500, 'Internal error - /recommendation')


def make_response(status_code, body):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': HEADERS
    }
