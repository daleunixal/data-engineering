import json
import pickle
import sqlite3


def parse_data_pkl(file_name):
    with open(file_name, "rb") as file:
        data_file = pickle.load(file)

        for item in data_file:
            item.pop('acousticness')
            item.pop('energy')
            item.pop('popularity')

    return data_file


def parse_data_txt(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        line = file.readlines()

        data_file = []
        item = dict()

        for row in line:
            if row == "=====\n":
                data_file.append(item)
                item = dict()
            else:
                if row == "\n":
                    break

                row = row.strip().split("::")

                if row[0] in ["duration_ms", "year"]:
                    item[row[0]] = int(row[1])
                elif row[0] in ['tempo']:
                    item[row[0]] = float(row[1])
                elif row[0] in ['artist', 'genre', 'song']:
                    item[row[0]] = row[1]
                else:
                    continue
    return data_file


def connect_to_database(database):
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS music (
                id           INTEGER    PRIMARY KEY ASC,
                artist       TEXT (255),
                song         TEXT (255),
                duration_ms  INTEGER,
                year         INTEGER,
                tempo        REAL,
                genre        TEXT (255)
                )""")
    db.commit()


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre)
        VALUES(
            :artist, :song, :duration_ms, :year,
            :tempo, :genre
        )
    """, data)

    db.commit()


def get_top_by_year(db):
    cursor = db.cursor()

    res = cursor.execute(
        "SELECT * FROM music ORDER BY year DESC LIMIT 15")
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def statistical_characteristics(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(duration_ms) as min,
        MAX(duration_ms) as max,
        AVG(duration_ms) as avg,
        SUM(duration_ms) as sum
        FROM music
    """)

    res = res.fetchone()
    cursor.close()

    print(dict(res))

    return []


def tag_frequency(db):
    cursor = db.cursor()

    result_tag = cursor.execute("""
                    SELECT
                        CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
                        artist
                    FROM music
                    GROUP BY artist

    """)

    for row in result_tag.fetchall():
        print(dict(row))
    cursor.close()

    return []


def get_top_by_duration_ms(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM music 
        WHERE duration_ms > 221933
        ORDER BY tempo DESC LIMIT 15
        """)

    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


items = parse_data_pkl('./task_3_var_06_part_2.pkl') + parse_data_txt('./task_3_var_06_part_1.text')
database = connect_to_database("./results/first.db")
create_table(database)
# insert_data(db, items)

res_1 = get_top_by_year(database)
res_2 = get_top_by_duration_ms(database)

with open('./results/r_task3.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_1, ensure_ascii=False))

with open('./results/r_task3_filter.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_2, ensure_ascii=False))

statistical_characteristics(database)
tag_frequency(database)
