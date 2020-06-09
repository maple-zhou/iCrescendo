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


sql1 = 'SELECT * FROM Singers'
cursor.execute(sql1)
# get all information of singers
result1 = cursor.fetchall()
num1 = len(result1)
print("Get all information.")

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
      },
    },
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "long",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "name": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "singer url": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "album number": {
        "type": "long",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "albums": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "country": {
        "type": "text",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "total comments": {
        "type": "long",
        "analyzer": "ik_smart",
        "search_analyzer": "ik_smart",
      },
      "img": {
        "type": "text",
      },
    }
  }
}

# create singer index
res = es.indices.create(index="singer", body=mappings, ignore=400)


def create_singer_index(result, id):
    name = result[0][1]
    singer_url = result[0][2]
    album_number = result[0][3]
    album_ids = result[0][4]
    li_album_ids = eval(album_ids)
    album = []
    for j in range(len(li_album_ids)):
        sql = 'SELECT * FROM Albums WHERE id=%s'
        cursor.execute(sql, int(li_album_ids[j]))
        ans = cursor.fetchall()
        if len(ans) != 0:
            album_name = ans[0][1]
            issue_date = ans[0][3]
            album.append((album_name, issue_date))
    country = result[0][5]
    total_comments = result[0][6]
    img = result[0][7]
    body = {"name": name,
            "singer url": singer_url,
            "album number": album_number,
            "albums": str(album),
            "country": country,
            "total comments": total_comments,
            "img": img}
    # create doc
    es.index(index="singer", id=id, body=body)
    return


sql2 = 'SELECT id FROM Singers'
cursor.execute(sql2)
# get all id of singers
result2 = cursor.fetchall()

for i in range(len(result2)):
    id = int(result2[i][0])
    sql1 = 'SELECT * FROM Singers WHERE id={}'.format(id)
    cursor.execute(sql1)
    # get all info of singers
    result1 = cursor.fetchall()
    create_singer_index(result1, id)
    print(i, "done")

print("Finish!")
