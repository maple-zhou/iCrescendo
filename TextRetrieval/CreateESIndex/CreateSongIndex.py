import pymysql
from elasticsearch import Elasticsearch

# connect to mySQL
conn = pymysql.connect(host='xxx',
                       port=3306,
                       user="xxx",
                       passwd="xxx",
                       db='xxx',
                       charset="utf8mb4")
cursor = conn.cursor()
print("Connect to mySQL!")

# Connect to Elasticsearch
es = Elasticsearch(['xxx'], ignore=400)
print(es.ping())

# mappings & analyzers
mappings = {
  "settings": {
    "analysis": {
      "char_filter": {
        "&_to_and": {
          "type": "mapping",
          "mappings": ["&=> and"]
        }
      },
      "filter": {
        "my_stopwords": {
          "type": "stop",
          "stopwords": ["the"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "long",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "song name": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "song url": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "cover": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "lyrics": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "commentnum": {
        "type": "long",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "comments": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "lyrics common words": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "comments common words": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "singer": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
    }
  }
}

# create song index
res = es.indices.create(index="song", body=mappings, ignore=400)        # create index


def create_song_index(result, id):
    song_name = result[0][1]
    song_url = result[0][2]
    cover = result[0][3]
    lyrics = result[0][4]
    commentnum = result[0][5]
    comments = result[0][6]
    lyrics_common_words = result[0][7]
    comments_common_words = result[0][8]
    singer = result[0][9]
    body = {"song name": song_name,
            "song url": song_url,
            "cover": cover,
            "lyrics": lyrics,
            "commentnum": commentnum,
            "comments": comments,
            "lyrics common words": lyrics_common_words,
            "comments common words": comments_common_words,
            "singer": singer}
    # create doc
    es.index(index="song", id=id, body=body)


sql2 = 'SELECT id FROM Songs'
cursor.execute(sql2)
# get all id of songs
result2 = cursor.fetchall()

for i in range(len(result2)):
    id = int(result2[i][0])
    sql3 = 'SELECT * FROM Songs WHERE id = {}'.format(id)
    cursor.execute(sql3)
    # get info of song
    result3 = cursor.fetchall()
    num3 = len(result3)
    print(i, 'done')
    create_song_index(result3, id)

print("Finish!")
