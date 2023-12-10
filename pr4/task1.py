import json
import msgpack
import sqlite3

from pr5.utils.generalPurposeReader import get_object_list
from pr5.utils.jsonDumper import json_dump


def parse_data(file_name):
    with open(file_name, "rb") as file:
        data_file = msgpack.load(file)
    return data_file


def connect_to_database(database):
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS building (
            id           INTEGER PRIMARY KEY ASC,
            name         TEXT (255),
            street       TEXT (255),
            city        TEXT (255),
            zipcode       INTEGER,
            floors      INTEGER,
            year        INTEGER,
            parking      INTEGER,
            prob_price    INTEGER,
            views           INTEGER
            
            )""")
    db.commit()


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO building (name, street,  city, zipcode, floors, year, parking, prob_price, views )
        VALUES(
            :name, :street, :city, :zipcode, :floors,
            :year, :parking, :prob_price, :views
        )
    """, data)

    db.commit()


def get_top_by_tours_count(db):
    cursor = db.cursor()

    res = cursor.execute(
        "SELECT * FROM building ORDER BY floors DESC LIMIT 15")
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(dict(row))
    cursor.close()

    return items_list


def get_top_by_min_rating(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM building 
        WHERE views > 3400
        ORDER BY zipcode DESC LIMIT 15
        """)

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
        MIN(views) as min,
        MAX(views) as max,
        AVG(views) as avg,
        SUM(views) as sum
        FROM building
    """)

    items = []
    res = res.fetchone()
    items.append(dict(res))
    cursor.close()
    return items


items = get_object_list('./task_1_var_06_item.msgpack')

print(items)


def tag_frequency(db):
    cursor = db.cursor()

    result_tag = cursor.execute("""
                    SELECT
                        CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM building) as count,
                        city
                    FROM building
                    GROUP BY city
                
    """)

    items = []
    for row in result_tag.fetchall():
        items.append(dict(row))
    cursor.close()
    return items


db = connect_to_database("./results/first.db")
create_table(db)
# insert_data(db, items)

st = statistical_characteristics(db)
tag = tag_frequency(db)
json_dump(st, 'r_t1_1')
json_dump(tag, 'r_t1_2')

res_1 = get_top_by_tours_count(db)
res_2 = get_top_by_min_rating(db)

with open('./results/r_task1.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_1, ensure_ascii=False))

with open('./results/r_task1_filter.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_2, ensure_ascii=False))
