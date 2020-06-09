import jieba
import pymysql
from collections import Counter
import re


def remove_stop_words(f):
    stop_words = ['作词', '总比', '要会', '居然', '冒泡', '哈哈',  '作曲', '编曲', 'Arranger', '录音', '混音', '人声', 'Vocal', '弦乐', 'Keyboard', '键盘', '编辑', '助理',
                  'Assistants', '或是', 'Mixing', 'Editing', 'Recording', '音乐', '制作', 'Producer', '发行', 'produced', 'and',
                  'distributed', '居然', '已经', '还入', '好久没', '听倪', '反正', '总监', 'studio', 'Recorded', 'Art', '文化传媒',
                  'Studio', '母带', '没有', '评论', '怎么', '一个', '回复', '这般', '..', '...', '__', '___', '......', '一句',
                  '什么', '因为', '首歌', '可爱', '大哭', '生病', '大笑', '顶顶', '突然', '奸笑', '而且', '一般', '有种', '这歌',
                  '汗', '发现', '我', '你', '你们', '他', '她', '不是', '不好', '这首', '一种', '真的', '方式', '难道', '换个',
                  '一首', '所有', '后面', '破破', '憨笑', '卧槽', '如果', '但是', '不能', '竟然', '煞笔', '几年', '这货', '撇嘴',
                  '明显', '像是', '还是', '一样', '知道', '听到', '那个', '叽叽', '那么', '哈哈哈', '还是', '大家', '可以',
                  '这里', '总会', '啊啊啊', '多多', '999', '高中', '时候', '个人', '这么', '这种', '认为', '这个', '有人',
                  '生气', '来看', '爱心', '觉得', '一天', '就是', '钻石', '惊恐', '愉快', '妩媚', '天真', '猖狂', '心碎']
    for stop_word in stop_words:
        f = f.replace(stop_word, "")
    return f


def creat_cut_text(f):
    if f == 'null':
        return 'null'
    common_word = []
    f = re.sub('[a-zA-Z]', '', f)
    f = remove_stop_words(f)
    seg_list = jieba.cut(f, cut_all=False, HMM=True)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\r\n':
            c[x] += 1
    for (k, v) in c.most_common(6):
        common_word.append(k)
    res = str(common_word)
    if res == []:
        res = None
    return res


conn = pymysql.connect(host='121.199.77.180', port=3306, user='root', passwd='Zrh999999', db='NeteaseCloudMusic', charset="utf8mb4")
cursor = conn.cursor()
print("Connect!")

sql2 = 'SELECT id FROM Songs'
cursor.execute(sql2)
# get all id of songs
result2 = cursor.fetchall()

for i in range(len(result2)):
    id = int(result2[i][0])
    sql = 'SELECT id, comments FROM Songs WHERE id={}'.format(id)
    cursor.execute(sql)
    res = cursor.fetchall()
    ans = creat_cut_text(str(res[0][1]))
    print(i, ans)
    # cursor.execute('alter table Songs add column `comments common words` VARCHAR(300);')
    cursor.execute('UPDATE `Songs` SET `comments common words`=%s WHERE `id`=%s', (ans, id))
    if not (i % 1000):
        conn.commit()
else:
    conn.commit()

print("Finish!")
