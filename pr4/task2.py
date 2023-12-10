import json
import sqlite3

from pr5.utils.generalPurposeReader import get_object_list


def connect_to_db(db):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS building_subitem (
         id           INTEGER PRIMARY KEY ASC,
         id_building  INTEGER REFERENCES building (id),
         name         TEXT (255),
         place        INTEGER,
         prise        INTEGER
        )
    """)


def insert_subitem_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
           INSERT INTO building_subitem (id_building, name, place, prise)
           VALUES(
                (SELECT id FROM building WHERE name = :name),
                :name, :place, :prise
           )
       """, data)

    db.commit()


def first_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
        SELECT * 
        FROM building_subitem
        WHERE id_building = (SELECT id FROM building WHERE name = ?) 
     """, [name])

    for row in res.fetchall():
        item = dict(row)
        print(item)

    cursor.close()
    return []


def second_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
           SELECT
                AVG(place) as avg_place, 
                AVG(prise) as avg_prise
           FROM building_subitem
           WHERE id_building = (SELECT id FROM building WHERE name = ?) 
        """, [name])

    print(dict(res.fetchone()))

    cursor.close()
    return []


def third_query(db, name):
    cursor = db.cursor()
    res = cursor.execute(""" 
           SELECT *
           FROM building_subitem
           WHERE id_building = (SELECT id FROM building WHERE name = ?) 
           ORDER BY prise DESC 
        """, [name])

    for row in res.fetchall():
        print(dict(row))

    cursor.close()
    return []


items = get_object_list('./task_2_var_06_subitem.pkl')
database = connect_to_db("./results/first.db")
create_table(database)
# insert_subitem_data(database, items)
first_query(database, 'Дортмунд 1969')
second_query(database, 'Гран-при ФИДЕ 1977')
third_query(database, 'Ставангер 1961')
