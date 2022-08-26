import pymysql
import pymysql.cursors

connection = pymysql.connect(host='127.0.0.1', port=3306, user='''''', password='hogehoge-123', db='''''')
# userとdbはそれぞれに設定してください
# この関数の呼び出しによって、データベースとの接続が確立されます。

with connection.cursor() as cursor:
    sql = "SELECT hoge_calumn FROM hoge_table"
    # SQL命令文です。ここは適宜変えてください

    cursor.execute(sql)
    #pymysqlはこの関数の呼び出しによって、SQL命令文の実行が行われます。

    connection.commit()
    #データベースに変更を加えるようなSQL命令文を実行した時にはこの関数を呼び出して同期をします

    result = cursor.fetchall()
    #SQL命令文の結果が欲しい場合にはこの関数を呼び出します。
    #結果を受け取る関数は他にもあるので、調べてみてください。

    connection.close()
    #データベースへの接続を切ります。この関数を呼び出さないとデータベースがずっと待ち続けるので、書いておいてください。
