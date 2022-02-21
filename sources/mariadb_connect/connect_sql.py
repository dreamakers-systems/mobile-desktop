from os.path import join, dirname, realpath
import mariadb
import csv
import sys
import os

from settings import PROJECT_PATH


class ConnectSql():
    def __init__(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="admin",
                host="localhost",
                port=3306,
                database='base_g4')
            # print('base de dados conectada')
            #self.conn.autocommit = False
            self.cursor = self.conn.cursor()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def commit_db(self): 
        self.conn.commit()

    def close_db(self): 
        self.conn.close()

def create_sql_table():
    connect = ConnectSql()
    for file in os.listdir(join(PROJECT_PATH, 'data_csv')):
        # scheme_ = 
        connect.cursor.execute("CREATE TABLE IF NOT EXISTS {}(" \
            "date_time DATETIME UNIQUE, " \
            "valor INTEGER(11) NOT NULl, " \
            "operator VARCHAR(1));".format(file[:-4].replace(" ", "_")))
        connect.commit_db()
    connect.close_db()

def insert_data():
    connect = ConnectSql()
    for file in os.listdir(join(PROJECT_PATH, 'data_csv')):
        csv_archive = csv.reader(open(
            os.path.join(PROJECT_PATH,'data_csv', file), 'rt'), delimiter=',')

        for line in csv_archive:
            scheme_ = "INSERT IGNORE INTO {}" \
                "(date_time, valor, operator)" \
                "VALUES ('{}','{}','{}')".format(
                    file[:-4].replace(" ", "_"), line[0], line[1], line[2])
            connect.cursor.execute(scheme_)
    connect.commit_db()
    
def show_tables():
    connect = ConnectSql()
    connect.cursor.execute(
        "select table_name \
        FROM information_schema.tables \
        WHERE table_schema = 'base_g4';")
    list_ = [tables[0] for tables in connect.cursor.fetchall()]
    connect.close_db()
    return list_

def search_runs(table_name, initial_date, final_date):
    connect = ConnectSql()
    connect.cursor.execute(
        "SELECT DATE_FORMAT(date_time, '%d-%m-%Y %H:%i'), valor, operator \
        FROM base_g4.{} \
        WHERE date_time \
        BETWEEN '{}' AND '{}';".format(table_name, initial_date, final_date))
    list_ = [[tables[0], tables[1], tables[2]]
        for tables in connect.cursor.fetchall()]
    connect.close_db()
    return list_

    


    

    
