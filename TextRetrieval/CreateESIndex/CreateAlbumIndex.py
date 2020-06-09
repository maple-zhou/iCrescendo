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
        "ablum name": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "album url": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "issue date": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "introduction": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "cover": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "singer": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "songs": {
            "type": "text",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        },
        "album comments": {
            "type": "long",
            "analyzer": "ik_smart",
            "search_analyzer": "ik_smart",
        }
    }
  }
}

# create album index
res = es.indices.create(index="album", body=mappings, ignore=400)        # create index


def create_album_index(result, id):
    if len(result[0]) == 0:
        return
    album_id = result[0][0]
    album_name = result[0][1]
    album_url = result[0][2]
    issue_date = result[0][3]
    introduction = result[0][4]
    cover = result[0][5]
    singer = result[0][6]
    song_ids = result[0][7]
    li_song_ids = eval(song_ids)
    song = []
    for j in range(len(li_song_ids)):
        sql = 'SELECT * FROM Songs WHERE id=%s'
        cursor.execute(sql, int(li_song_ids[j]))
        ans = cursor.fetchall()
        if len(ans) != 0:
            song_name = ans[0][1]
            song.append(song_name)
    album_comments = result[0][8]
    body = {"album name": album_name,
            "album url": album_url,
            "issue date": issue_date,
            "introduction": introduction,
            "cover": cover,
            "singer": singer,
            "songs": str(song),
            "album comments": album_comments}
    # create doc
    es.index(index="album", id=album_id, body=body)
    return


sql2 = 'SELECT id FROM Albums'
cursor.execute(sql2)
# get all id of albums
result2 = cursor.fetchall()

for i in range(len(result2)):
    id = int(result2[i][0])
    sql2 = 'SELECT * FROM Albums WHERE id = {}'.format(id)
    cursor.execute(sql2)
    # get info of album
    result2 = cursor.fetchall()
    create_album_index(result2, id)
    print(i, 'done')

print("Finish!")
