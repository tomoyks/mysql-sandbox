import os
import MySQLdb.cursors

from enum import Enum


DB_CONNECTION = None


class DB_CONNECTION_ARGS(Enum):
    HOST: str = '127.0.0.1'
    PORT: str = '43306'
    USER: str = 'root'
    PASSWORD: str = ''
    DB: str = 'sakila'


def make_db_connection_args():
    """接続情報の辞書を作成する。"""
    args = {
        'host': os.getenv('MYSQL_HOST', DB_CONNECTION_ARGS.HOST.value),
        'port': int(os.getenv('MYSQL_PORT', DB_CONNECTION_ARGS.PORT.value)),
        'user': os.getenv('MYSQL_USER', DB_CONNECTION_ARGS.USER.value),
        'password': os.getenv('MYSQL_PASS', DB_CONNECTION_ARGS.PASSWORD.value),
        'db': os.getenv('MYSQL_DBNAME', DB_CONNECTION_ARGS.DB.value)
    }

    return args


def get_db_connection():
    """DBのコネクションを返す。"""
    global DB_CONNECTION

    if DB_CONNECTION is None:
        db_connection_args = make_db_connection_args()
        mysql_conn = MySQLdb.connect(**db_connection_args,
                                     charset='utf8mb4',
                                     cursorclass=MySQLdb.cursors.DictCursor,
                                     autocommit=True,
                                     )
        cur = mysql_conn.cursor()
        cur.execute(
            "SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'")
        DB_CONNECTION = mysql_conn

    return DB_CONNECTION


def get_table_info():
    """SHOW TABLESの結果を取得する。"""
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            sql = "SHOW TABLES"
            c.execute(sql)
            tables = c.fetchall()

    except MySQLdb.Error as err:
        print(err)
        return None

    return tables


def get_record_count(table_name):
    """テーブルのレコード数を取得する。"""
    conn = get_db_connection()
    try:
        with conn.cursor() as c:
            sql = "SELECT COUNT(*) FROM %s" % table_name
            c.execute(sql)
            number_of_rows = c.fetchone()

    except MySQLdb.Error as err:
        print(err)
        return None
    return number_of_rows['COUNT(*)']


def show_tables(table_name):
    """DESCRIBE {TABEL_NAME}で表示される内容を標準出力する。"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DESCRIBE %s" % table_name
            cursor.execute(sql)
            results = cursor.fetchall()

            widths = []
            columns = []
            tavnit = '|'
            separator = '+'

            for cd in cursor.description:
                widths.append(max(cd[2], len(cd[0])))
                columns.append(cd[0])

            for w in widths:
                tavnit += " %-"+"%ss |" % (w,)
                separator += '-'*w + '--+'

            print(separator)
            print(tavnit % tuple(columns))
            print(separator)
            for row in results:
                print(tavnit % tuple(row.values()))
            print(separator)

    except MySQLdb.Error as err:
        print(err)
        return None


if __name__ == '__main__':

    for table_info in get_table_info():
        table_name = table_info.get(f'Tables_in_{DB_CONNECTION_ARGS.DB.value}')
        
        record_count = get_record_count(table_name)
        print(f'■{table_name.upper()}: {record_count} records')

        show_tables(table_name)

        print('\n')