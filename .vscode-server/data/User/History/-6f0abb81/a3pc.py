from ast import Delete
from re import search
from sqlite3 import Cursor
import pymysql  # 参考: https://pymysql.readthedocs.io/en/latest/index.html
import pymysql.cursors
import logging
# from search_intern import Search

# ログの設定
format = "%(asctime)s: %(levelname)s: %(pathname)s: line %(lineno)s: %(message)s"
logging.basicConfig(filename='/var/log/intern3/flask.log', level=logging.DEBUG, format=format, datefmt='%Y-%m-%d %H:%M:%S')

connection = pymysql.connect(host='127.0.0.1',
                            user='intern3',
                            password='hogehoge-123',
                            port=3306,
                            database='intern3',
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)

class Database:
    def __init__(self):
        return
    
    # 料理とカロリーをDBに格納する
    def Insert(self, ary1, ary2,userId):
        # length = len(ary1)
        
        # search = Search()
        connection = pymysql.connect(host='127.0.0.1',
                        user='intern3',
                        password='hogehoge-123',
                        port=3306,
                        database='intern3',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:

                # delete = "DELETE FROM main_table;"
                # cursor.execute(delete)
                
                for i in range(len(ary1)):
                    # logging.debug(i)
                    sql = "INSERT INTO main_table (name, cal) VALUES (%s,%s);"
                    cursor.execute(sql, (ary1[i], ary2[i],))
                    if i >= 3:
                        break
                # logging.debug(sql)
                id = connection.insert_id()
                connection.commit()

                # ユーザー情報がない場合、ユーザー情報を格納する
                if self.userIn(userId) == False:
                    sql = "INSERT INTO user (userId,cal) VALUES (%s ,0) ;"
                    cursor.execute(sql,(userId))
                    connection.commit()
                    # logging.debug('aaa')

                # logging.debug(cursor.lastrowid)

                sql = "SELECT name FROM main_table WHERE id >= %s"
                cursor.execute(sql,(id))
                connection.commit()

                result = cursor.fetchall()
                logging.debug(result)


        finally:
            connection.close()

        return id, result

    # idから料理名を取得する
    def get_name(self,id_result):
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT name FROM main_table WHERE id = %s;"
                cursor.execute(sql,(id_result))

                connection.commit()

                result = cursor.fetchone()
        finally:
            connection.close()
        
        logging.debug(result)
        return result
    
    # idからカロリーを取得する
    def get_cal(self,id_result):
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT cal FROM main_table WHERE id = %s;"
                cursor.execute(sql,(id_result))

                connection.commit()

                cal_result = cursor.fetchone()
        finally:
            connection.close()
        
        return cal_result

    #userIdが既に入っていたらTrue
    def userIn(self, userId):
        flag = True
        
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
        
        try:
            with connection.cursor() as cursor:
                sql = "SELECT userId FROM user WHERE userId = %s;"
                cursor.execute(sql,(userId))
                connection.commit()

                result = cursor.fetchone()
                logging.debug(result)
                if result == None:
                    flag = False
                    
        finally:
            connection.close()
        return flag
    
    # calに何も入っていない時True
    def cal_check(self,userId):
        flag = False
        # logging.debug(userId)
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT cal FROM user WHERE userId = %s;"
                cursor.execute(sql,(userId))
                connection.commit()

                result = cursor.fetchone()
                if result == {'cal':0}:
                    flag = True
                    # logging.debug(flag)
                
        finally:
            connection.close()
        # logging.debug(flag)
        return flag

    # ユーザーが料理名を確定したらDBに格納する
    def cal_in(self,cal_result,userId):
        logging.debug(cal_result)
        logging.debug(userId)

        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE user SET cal  = %s WHERE userId = %s;"
                logging.debug(sql)
                r  = cursor.execute(sql,(cal_result,userId))
                connection.commit()
                logging.debug(r)
        finally:
            connection.close()
        
    # userIdからカロリーを取得する
    def id_cal(self,userId):
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT cal FROM user WHERE userId =%s;"
                cursor.execute(sql,(userId))
                connection.commit()

                result = cursor.fetchone()
                logging.debug(result)
        finally:
            connection.close()
        
        return result
        
    # 運動量を返したらユーザー情報を削除する
    def del_row(self,userId):
        connection = pymysql.connect(host='127.0.0.1',
                user='intern3',
                password='hogehoge-123',
                port=3306,
                database='intern3',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM user WHERE userId =%s;"
                cursor.execute(sql,(userId))
                connection.commit()

        finally:
            connection.close()

        