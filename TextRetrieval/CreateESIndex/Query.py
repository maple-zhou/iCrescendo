import json
from elasticsearch import Elasticsearch

es = Elasticsearch(['xxx'], ignore=400)
print(es.ping())
# test whether launch


def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
    return


# query for singer
query1 = {
    "query": {
        "match": {
          "name": "周"
        }
    },
    "sort": {
        "_score": {
            "order": "desc"
        },
        "total comments": {
            "order": "desc"
        }
    }
}

result = es.search(index="singer", body=query1, ignore=400)
json_print(result)


# query for album
query2 = {
    "query": {
        "match": {
          "album name": "范特西"
        }
    },
    "sort": {
        "_score": {
            "order": "desc"
        },
        "album comments": {
            "order": "desc"
        }
    }
}

result = es.search(index="album", body=query2, ignore=400)
json_print(result)

# query for song
query3 = {
    "query": {
        "match": {
          "song name": "七里"
        }
    },
    "sort": {
        "_score": {
            "order": "desc"
        },
        "commentnum": {
            "order": "desc"
        }
    }
}

result = es.search(index="song", body=query3, ignore=400)
json_print(result)
