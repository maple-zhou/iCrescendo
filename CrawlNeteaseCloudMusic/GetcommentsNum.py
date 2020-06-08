from retrying import retry
import json
from Crypto.Cipher import AES
import base64
import requests

# Decoding: to get the comments number of every song in the album
# params & encSecKey解密:获得专辑中每首歌曲的评论数
# second param
second_param = "010001"
# third_param 
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
# fourth param
forth_param = "0CoJUm6Qyw8W8jud"


def AES_encrypt(text, key, iv):
    if type(text) != bytes:
        text = text.encode("utf-8")
    if type(key) != bytes:
        key = key.encode("utf-8")
    if type(iv) != bytes:
        iv = iv.encode("utf-8")
    pad = 16 - len(text) % 16
    text = text.decode() + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    text = text.encode("utf-8")
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text


# page为传入页数
def get_params(page):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'F'
    if(page == 1): 
        # offset的取值为:(评论页数-1)*20,total第一页为true，其余页为false
        first_param = '{rid:"", offset:"0", total:"true", limit:"20", csrf_token:""}'
        h_encText = AES_encrypt(first_param, first_key, iv)
    else:
        offset = str((page-1)*20)
        first_param = '{rid:"", offset:"%s", total:"%s", limit:"20", csrf_token:""}' % (offset, 'false')
        h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText


def get_encSecKey():
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
    return encSecKey


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def get_json(url, params, encSecKey):
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                        AppleWebKit/537.36 (KHTML, like Gecko)\
                         Chrome/81.0.4044.92 Safari/537.36',
               'Cookie': 'appver=1.5.0.75771;',
               'Referer': 'http://music.163.com/'}
    proxies = {
            'http:': 'http://121.232.146.184',
            'https:': 'https://144.255.48.197'
    }
    data = {
         "params": params,
         "encSecKey": encSecKey
    }
    response = requests.post(url, headers=headers, data=data, proxies=proxies)
    return response.content

# get the number of comments of the song
def getcommentNum(song_id, headers):
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])
    return comments_num

# get the hottest 10 comments of the song
def getcomment(song_id, headers):
    comments = []
    url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
    params = get_params(1)
    encSecKey = get_encSecKey()
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    for item in json_dict['hotComments']:
        comments.append(item['content'])
    for item in json_dict['comments'][0:10]:
        comments.append(item['content'])
    return comments
