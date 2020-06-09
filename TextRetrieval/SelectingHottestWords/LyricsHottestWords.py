import jieba
import pymysql
from collections import Counter
import re
import nltk


def remove_chinese_stop_words(f):
    # add your Chinese stop words here
    stop_words = ['作词', '曲编', '搬运', '原唱', '钢琴伴奏', '作曲', '编曲', '录音', '混音', '人声', '弦乐', '键盘', '编辑', '助理',
                  '音乐', '制作', '发行', '总监', '文化传媒', '母带', '多少', '我们', '所有', '一种', '几成', '一次', '一场', '一段',
                  '纷纷', '有', '没有', '有没有', '那些', '不到', '什么', '我', '你们', '一个', '这请', '才能', '还是', '因为', '一直',
                  '仿佛', '好像', '这么', '是', '不是', '可以', '不可以', '是否', '专辑', '暂无', '歌词', '乐队', '曲绘', '词曲',
                  '手游', '主题曲', '美工', '歌曲', '填词', '舞曲', '欣赏', '乐队', '文本', '琵琶', '监制', '打击乐', '笛子', '念白', '策划',
                  '文案', '贝斯', '爵士鼓', '萨克斯风', '旁白', '群星', '翻唱', '演唱', '主唱', '原唱', '编写', '处理', '视频剪辑',
                  '统筹', '电视剧', '插曲', '片尾曲', '版本', '电音', '享版', '公司', '环球', '出版', '文化', '执行',
                  '间奏', '工程', '片头曲', '合唱', '交响乐', '国际', '首席', '爱乐乐团', '配器', '二胡',
                  '萨克斯风', '企划', '后期', '前奏', '封面设计', '极了', '出品']
    for stop_word in stop_words:
        f = f.replace(stop_word, "")
    return f


def remove_english_stop_words(f):
    # add your English stop words here
    stop_words = ['executive', 'arranged', 'guitars', 'recorded', 'ourselves', 'publishing', 'op', 'production', 'sp',
                  'admin', 'producer', 'backing', 'live', 'top', 'cv', 'bgm', 'hers', 'between', 'yourself', 'but',
                  'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'this', 'they',
                  'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'wasn',
                  'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each',
                  'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'engineer',
                  'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our',
                  'their', 'recording', 'strings', 'while', 'above', 'tie', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when',
                  'record', 'background', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
                  'yourselves', 'yan', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'rap',
                  'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'mc', 'which', 'wd', 'music', 'backing',
                  'mixing', 'young', 'im', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against',
                  'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than', 'Arranger', 'Vocal', 'Keyboard',
                  'Assistants', 'Mixing', 'Editing', 'Recording', 'Producer', 'produced', 'and', 'mastering',
                  'distributed',  'studio', 'Recorded', 'Art', 'don', 'anymore', 'talk', 'PV', 'pv']
    filtered_sentence = [f[i] for i in range(len(f)) if f[i] not in stop_words]
    return filtered_sentence


def creat_cut_text(f):
    if f == 'null':
        return 'null'
    common_word = []
    # using re to separate Chinese & English
    Chinese_str = re.sub('[a-zA-Z]', '', f)
    English_str = re.sub('[^a-zA-Z]', ' ', f)
    english_list = list(nltk.word_tokenize(English_str.lower()))
    Chinese_str = remove_chinese_stop_words(Chinese_str)
    english_list = remove_english_stop_words(english_list)
    seg_list = jieba.cut(Chinese_str, cut_all=False, HMM=True)
    seg_list = list(seg_list)
    seg_list.extend(list(english_list))
    # print("统计词频！")
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    # print('常用词频度统计结果')
    for (k, v) in c.most_common(6):
        common_word.append(k)
    if len(common_word) == 0:
        return "null"
    return str(common_word)


conn = pymysql.connect(host='xxx', port=3306, user='xxx', passwd='xxx', db='xxx', charset="utf8mb4")
cursor = conn.cursor()

sql2 = 'SELECT id FROM Songs'
cursor.execute(sql2)
# get all id of songs
result2 = cursor.fetchall()

for i in range(len(result2)):
    id = int(result2[i][0])
    sql = 'SELECT id, lyrics FROM Songs WHERE id={}'.format(id)
    cursor.execute(sql)
    res = cursor.fetchall()
    string = creat_cut_text(str(res[0][1]))
    print(i, string)
    cursor.execute('UPDATE `Songs` SET `lyrics common words`=%s WHERE `id`=%s', (string, id))
    if not (i % 1000):
        conn.commit()
else:
    conn.commit()

# cursor.execute('alter table Songs add column `lyrics common words` VARCHAR(300);')
print("Finish!")
