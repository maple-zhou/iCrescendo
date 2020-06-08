import CrawlNeteaseCloudMusic as Crawl
import pymysql


def CreateTables(conn, cursor):
    cursor.execute('drop TABLE if exists Singers')
    cursor.execute('drop TABLE if exists Albums')
    cursor.execute('drop TABLE if exists Songs')
    conn.commit()
 
    # create singer table
    cursor.execute('CREATE TABLE `Singers`(\
                   `id` VARCHAR(100) NOT NULL,\
                   `name` VARCHAR(100) NOT NULL,\
                   `url` VARCHAR(100) NULL,\
                   `album number` INT NULL,\
                   `albums id` VARCHAR(2000) NULL,\
                   `country` VARCHAR(45) NULL,\
                   `total comments` BIGINT NULL,\
                   `img` VARCHAR(200),\
                   PRIMARY KEY(`id`),\
                   INDEX `ID` USING BTREE(`id`))\
                   ENGINE = InnoDB,\
                   DEFAULT CHARACTER SET = utf8mb4')
    conn.commit()
    # create album table
    cursor.execute('CREATE TABLE `Albums`(\
                   `id` VARCHAR(100) NOT NULL,\
                   `name` VARCHAR(100) NOT NULL,\
                   `url` VARCHAR(100) NULL,\
                   `issue date` VARCHAR(100) NULL,\
                   `introduction` VARCHAR(10000)NULL,\
                   `cover` VARCHAR(200) NULL,\
                   `singer` VARCHAR(200) NULL,\
                   `songs` VARCHAR(2000) NULL,\
                   `album comments` BIGINT,\
                   PRIMARY KEY(`id`),\
                   INDEX `ID` USING BTREE(`id`))\
                   ENGINE = InnoDB,\
                   DEFAULT CHARACTER SET = utf8mb4')
    conn.commit()
    # create songs table
    cursor.execute('CREATE TABLE `Songs`(\
                   `id` VARCHAR(100) NOT NULL,\
                   `name` VARCHAR(100) NOT NULL,\
                   `url` VARCHAR(100) NULL,\
                   `cover` VARCHAR(200) NULL,\
                   `lyrics` VARCHAR(10000) NULL,\
                   `commentnum` BIGINT,\
                   `comments`(10000) NULL,\
                   `singer`VARCHAR(1000) NULL,\
                   PRIMARY KEY(`id`),\
                   INDEX `ID` USING BTREE(`id`))\
                   ENGINE = InnoDB,\
                   DEFAULT CHARACTER SET = utf8mb4')
    conn.commit()


if __name__ == '__main__':
    Crawl.request(Crawl.request_url.format(1003, 74))
    Crawl.traverse()
    for i in Crawl.urls[0:10]:
        Crawl.get_info(i[0], i[1], i[2])
    print("crawl data successfully")

    conn = pymysql.connect(host='xxx', port=3306, user='xxx', passwd='xxx', db='xxx', charset="utf8mb4")
    cursor = conn.cursor()
    CreateTables(conn, cursor)
    print("create table successfully")

    # write data into database
    # singer
    for index, line in enumerate(Crawl.singers_data):
        cursor.execute("INSERT IGNORE INTO Singers (`id`, `name`,`url`,`album number`,`albums id`,`country`,`total comments`, `img`)\
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", list(line.values()))
        if not (index % 1000):
            conn.commit()
    else:
        conn.commit()

    # album
    for index, line in enumerate(Crawl.albums_data):
        cursor.execute("INSERT IGNORE INTO Albums (`id`, `name`,`url`,`issue date`,`introduction`,`cover`,`singer`,`songs`,`album comments`)\
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", list(line.values()))
        if not (index % 1000):
            conn.commit()
    else:
        conn.commit()

    # song
    for index, line in enumerate(Crawl.songs_data):
        cursor.execute("INSERT IGNORE INTO Songs (`id`, `name`,`url`,`cover`,`lyrics`,`commentnum`, `comments`, `singer`)\
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", list(line.values()))
        if not (index % 1000):
            conn.commit()
    else:
        conn.commit()
    print("done")
