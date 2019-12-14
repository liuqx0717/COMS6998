import json
import boto3
import requests

headers = {
    "access-control-allow-origin": "*",
    "access-control-allow-headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "access-control-allow-methods": "GET,OPTIONS,PUT"
}


def search(q):
    """Lists the region and endpoint names of a particular partition.

    :type q: dict
    :param q: Keywords, price range and distance. All of them are OPTIONAL.
    :example q:
        q = {
          keyword: "string"
          priceMin: "number"
          priceMax: "number"
          distance: "number"
          lon: "number"
          lat: "number"
        }

    :return: Returns a list of item documents (type: dict).
    """

    es_endpoint = "https://search-e6998final-iijtdbqlcuarkxq23kyrqvmyii.us-east-1.es.amazonaws.com/item/_search"

    # Construct default query body, which returns ALL the documents.
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
                            "distance": "99999km",
                            "location": {
                                "lat": 40.7,
                                "lon": -74.0
                            }
                        }
                    },
                    {
                        "range": {
                            "price": {
                                "gte": 0,
                                "lte": 99999
                            }
                        }
                    }
                ]
            }
        }
    }

    if 'keyword' in q:
        query_body['query']['bool']['should'] = [
            {"match": {"title": q['keyword']}},
            {"match": {"description": q['keyword']}},
            {"match": {"category": q['keyword']}},
            {"match": {"tag": q['keyword']}}
        ]

    if 'priceMin' in q:
        query_body['query']['bool']['filter'][1]['range']['price']['gte'] = q['priceMin']

    if 'priceMax' in q:
        query_body['query']['bool']['filter'][1]['range']['price']['lte'] = q['priceMax']

    if 'distance' in q:
        query_body['query']['bool']['filter'][0]['geo_distance']['distance'] = str(str(q['distance']) + 'km')

    if 'lat' in q and 'lon' in q:
        query_body['query']['bool']['filter'][0]['geo_distance']['location']['lat'] = q['lat']
        query_body['query']['bool']['filter'][0]['geo_distance']['location']['lon'] = q['lon']

    header = {
        "Content-Type": "application/json"
    }

    response = requests.get(url=es_endpoint, data=json.dumps(query_body), headers=header).json()
    print("response = ", json.dumps(response, indent=4))

    # Process search result.
    if response['hits']['total']['value'] == 0:
        return 0
    else:
        results = []
        for hit in response['hits']['hits']:
            result = hit['_source']
            result['id'] = hit['_id']
            results.append(result)

        return results


def lambda_handler(event, context):
    res = search(event)
    if res == 0:
        rsp = {
            "status": 200,
            "text": ""
            # "headers": headers
        }
    else:
        rsp = {
            "status": 200,
            "text": json.dumps(res)
            # "headers": headers
        }

    print("rsp = ", rsp)
    return rsp

# Example raw response from es.

# Non-hit response.
# {
#     "took": 19,
#     "timed_out": false,
#     "_shards": {
#         "total": 5,
#         "successful": 5,
#         "skipped": 0,
#         "failed": 0
#     },
#     "hits": {
#         "total": {
#             "value": 0,
#             "relation": "eq"
#         },
#         "max_score": null,
#         "hits": []
#     }
# }

# Hit response.
# {
#     "took": 16,
#     "timed_out": false,
#     "_shards": {
#         "total": 5,
#         "successful": 5,
#         "skipped": 0,
#         "failed": 0
#     },
#     "hits": {
#         "total": {
#             "value": 1,
#             "relation": "eq"
#         },
#         "max_score": 0.0,
#         "hits": [
#             {
#                 "_index": "item",
#                 "_type": "_doc",
#                 "_id": "9t5hBW8BuM8LsOt4NT1Z",
#                 "_score": 0.0,
#                 "_source": {
#                     "available": 1,
#                     "sellerId": "safwe456d4dsa",
#                     "title": "Half-off the hotBar!",
#                     "description": "save this coupon and pay onsite!",
#                     "imageUrl": [
#                         "someurl1",
#                         "someurl2"
#                     ],
#                     "category": [
#                         "diary",
#                         "deli"
#                     ],
#                     "tag": [
#                         "plate",
#                         "food",
#                         "beef"
#                     ],
#                     "price": 8.99,
#                     "prvPrice": 15.99,
#                     "stock": 150,
#                     "location": {
#                         "lat": 40.12,
#                         "lon": -71.34
#                     }
#                 }
#             }
#         ]
#     }
# }
