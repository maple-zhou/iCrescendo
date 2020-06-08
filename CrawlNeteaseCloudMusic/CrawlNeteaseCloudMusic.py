import requests
import GetCommentsNum
from lxml import etree
import json
from retrying import retry
import pymysql
import re


# get the response
@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_page(url, headers):
    response = requests.get(url, headers=headers)
    return response.text

# create tree
@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_tree(url, headers):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    return etree.HTML(response.text)


# crawl all singers and their urls on a certain page
def request(start_url):
    tree = get_tree(start_url, headers)
    singer_li_list = tree.xpath('//ul[@id="m-artist-box"]/li')
    for li in singer_li_list:
        name = li.xpath('.//a[@class="nm nm-icn f-thide s-fc0"]/text()')[0]
        suffix = li.xpath('.//a[1]/@href')[0]
        id = suffix.split("id=")[1]
        url = basic_url + suffix
        singer_info = [id, name, url]
        urls.append(singer_info)


# traverse all kinds of singers
def traverse():
    # 1001: Chinese male singer, 1002: Chinese female singer, 1002: Chinese group
    id = [1001, 1002, 1003]
    # 65-90:A-Z
    initial = list(range(65, 91))
    initial.append(0)
    for i in id:
        for j in initial:
            request(request_url.format(i, j))


def song_lyric(song_id, headers):
    url_lyric = "http://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1".format(song_id)
    text = get_page(url_lyric, headers)
    # using re to examine whether the lyrics are null
    judge_lyric = re.findall(r'{"nolyric":true,.*?}', text, re.DOTALL)
    if judge_lyric:
        initial_lyric = 'null'
    else:
        # using json to get the lyrics of a song
        json_obj = json.loads(text)
        if 'lrc' in json_obj:
            initial_lyric = json_obj['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", initial_lyric)
            lrc = lrc.strip()
            return lrc
        else:
            initial_lyric = 'null'
    return initial_lyric


# crawl all info of a certain song: id, name, url, cover, lyrics, number of comments, 10 hottest comments, singer
def crawl_song(song_url, song_id):
    tree = get_tree(song_url, headers)
    song_cover = ''.join(tree.xpath('.//div[@class="u-cover u-cover-6 f-fl"]/img/@src'))
    song_name = tree.xpath('.//em[@class="f-ff2"]/text()')[0]
    commentnum = GetCommentsNum.getcommentNum(song_id, headers)
    comments = GetCommentsNum.getcomment(song_id, headers)
    song_lyrics = song_lyric(song_id, headers)
    singer = ''.join(tree.xpath('.//p[@class="des s-fc4"][1]/span//text()'))
    song_info = {'song id': song_id,
                 'name': song_name,
                 'url': song_url,
                 'cover': song_cover,
                 'lyrics': song_lyrics,
                 'commentnum': commentnum,
                 'comments': comments,
                 'singer': singer}
    json.dumps(song_info)
    songs_data.append(song_info)
    return commentnum


# crawl all info of an album
def crawl_album(album_url, album_id):
    songs_id = []
    tree = get_tree(album_url, headers)
    album_name = ''.join(tree.xpath('.//div[@class="tit"]/h2/text()'))
    album_time = ''.join(tree.xpath('.//p[@class="intr"][2]/text()'))
    album_cover = ''.join(tree.xpath('.//div[@class="cover u-cover u-cover-alb"]/img/@src'))
    # some introduction needs to expand, some not
    if (''.join(tree.xpath('.//div[@id="album-desc-more"]//text()'))):
        album_intro = ''.join(tree.xpath('.//div[@id="album-desc-more"]//text()'))
    else:
        album_intro = ''.join(tree.xpath('.//div[@id="album-desc-dot"]//text()'))


# eg.前一行：恋与白侍从/安筱冷  后一行：恋与白侍从 / 安筱冷  （/前后有无空格）
    singer = ''.join(tree.xpath('.//p[@class="intr"][1]/span//text()'))
    # singer = ''.join(tree.xpath('.//p[@class="intr"][1]/span//text()')).replace(" ","")

    songs_list = tree.xpath('.//meta[@property="og:music:album:song"]/@content')
    album_comments = 0
    for song_info in songs_list:
        song_url = song_info.split("url=")[1]
        song_id = song_url.split("id=")[1]
        songs_id.append(song_id)
        song_commentnum = int(crawl_song(song_url, song_id))
        album_comments += song_commentnum

    album_info = {'album id': album_id,
                  'name': album_name,
                  'url': album_url,
                  'issue date': album_time,
                  'introduction': album_intro,
                  'cover': album_cover,
                  'singer': singer,
                  'songs': str(songs_id),
                  'album comments': album_comments}
    json.dumps(album_info)
    albums_data.append(album_info)
    return album_comments


def get_info(id, name, url):
    country = ''
    album_number = 0
    albums_id = []
    tree = get_tree(url, headers)
    img = ''.join(tree.xpath('.//div[@class="n-artist f-cb"]/img/@src'))
    suffix = tree.xpath('//ul[@id="m_tabs"]/li[2]/a/@href')[0]
    page1_url = basic_url + suffix
    tree = get_tree(page1_url, headers)
    # get the url of each page of the album
    pages_of_url = [page1_url]
    for i in tree.xpath('//a[@class="zpgi"]/@href'):
        pages_of_url.append(basic_url + i)
    # get the url of every album
    albums_url = []
    for i in pages_of_url:
        tree = get_tree(i, headers)
        album_li_list = tree.xpath('//ul[@class="m-cvrlst m-cvrlst-alb4 f-cb"]/li')
        for li in album_li_list:
            album_number += 1
            suffix = li.xpath('.//p[@class="dec dec-1 f-thide2 f-pre"]/a/@href')[0]
            album_url = basic_url + suffix
            album_id = suffix.split("id=")[1]
            albums_url.append(album_url)
            albums_id.append(album_id)
    # crawl all info of every album
    total_comments = 0
    for i in range(album_number):
        album_comments = crawl_album(albums_url[i], albums_id[i])
        total_comments += album_comments
    singer_info = {'singer id': id,
                   'name': name,
                   'url': url,
                   'album number': album_number,
                   'albums id': str(albums_id),
                   'country': country,
                   'total comment': total_comments,
                   'img': img}
    json.dumps(singer_info)
    singers_data.append(singer_info)


headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                        AppleWebKit/537.36 (KHTML, like Gecko)\
                         Chrome/81.0.4044.92 Safari/537.36',
           'Cookie': 'appver=1.5.0.75771;',
           'Referer': 'http://music.163.com/'}
basic_url = "https://music.163.com"
request_url = "https://music.163.com/discover/artist/cat?id={}&initial={}"
singers_data = []
albums_data = []
songs_data = []
urls = []