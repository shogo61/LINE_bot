# Python 3.10.4
# Flask 2.1.2
# Flaskの公式ドキュメント：https://flask.palletsprojects.com/en/2.1.x/
# python3の公式ドキュメント：https://docs.python.org/ja/3.10/
# python3の基礎文法のわかりやすいサイト：https://note.nkmk.me/python/
# 使用するモジュールのインポート
# pythonが提供しているモジュールのインポート
import re
import json
import logging
import urllib.request
import requests
from flask import Flask, request
from flask.wrappers import Response
import math
# 自分で作成したモジュールのインポート
from search import Search
from database import Database

# Flaskクラスをnewしてappに代入
# gunicornの起動コマンドに使用しているのでここは変更しないこと
app = Flask(__name__)

# ログの設定
format = "%(asctime)s: %(levelname)s: %(pathname)s: line %(lineno)s: %(message)s"
logging.basicConfig(filename='/var/log/intern3/flask.log',
                    level=logging.DEBUG, format=format, datefmt='%Y-%m-%d %H:%M:%S')

# 「/」にPOSTリクエストが来た場合、index関数が実行される
@app.route('/', methods=['post'])
def index():
    # 以下のコードでログを出力できる。出力先は「ログの設定」にあるファイル。コマンドラインに出力する場合はprintを使う。
    # POSTリクエストのbodyを取得
    search = Search()
    db = Database()
    body_binary = request.get_data()
    body_decoded = json.loads(body_binary.decode())
    logging.debug(body_decoded)
    replyToken = body_decoded['events'][0]['replyToken']

    # 友達追加時の処理
    if body_decoded['events'][0]['type'] == 'follow':
        first_comment(replyToken)
        
    # ユーザーが料理名を選んだ時の処理
    if body_decoded['events'][0]['type'] == 'postback':
        userId = body_decoded['events'][0]['source']['userId']
        logging.debug(userId)

        id_result = body_decoded['events'][0]['postback']['data']
        logging.debug(id_result)

        name_result = db.get_name(id_result)['name']
        logging.debug(name_result)

        cal_result = db.get_cal(id_result)['cal']
        logging.debug(cal_result)

        #userIdにcalを格納する
        db.cal_in(cal_result, userId)
        replyToken = body_decoded['events'][0]['replyToken']
        logging.debug(replyToken)
        res_cal(replyToken, name_result, cal_result)

    # ユーザーがメッセージを送ってきた時の処理
    elif body_decoded['events'][0]['type'] == 'message':
        body_catch = body_decoded['events'][0]['message']['text']
        logging.debug(body_catch)
        userId = body_decoded['events'][0]['source']['userId']

        # calとuserIdに値が入っている時体重を取得する
        if db.cal_check(userId) == False and db.userIn(userId):
            weight = body_decoded['events'][0]['message']['text']
            # logging.debug(weight)
            try :
                #ここでエラー（文字列入力）が出たら例外処理
                weight = float(weight)
                # logging.debug(type(weight))

                # 体重を引数にして計算する処理
                cal_result = db.id_cal(userId)
                # replyToken = body_decoded['events'][0]['replyToken']
                logging.debug(replyToken)

                if(weight > 0):
                    motion = calc(cal_result, weight,replyToken)
                    res_motion(motion,replyToken,cal_result,weight)
                    # userのuserIdとcalを消す処理
                    db.del_row(userId)
                else:
                    # weightの値がマイナス
                    res_weight(replyToken)

            except ValueError:
                res_weight(replyToken)

        #calが０か、userIdが入っている時料理名を返す
        elif db.cal_check(userId) or db.userIn(userId) == False:
            ary1, ary2 = search.Search(body_catch)

            # 何も見つからなかった時
            if len(ary1) == 0:
                res_none(replyToken)
            else:
                id= db.Insert(ary1,ary2, userId)
                logging.debug(id)
                # logging.debug(type(ary))
                res(replyToken, id, ary1)

    return Response(status=200)



#料理名の候補を返す
def res(replyToken, id, ary1):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    contents = []
    if len(ary1) > 4:
        len_max = 3
    else:
        len_max = len(ary1) - 1
    logging.debug(id)
    for i in range(len(ary1)):
        logging.debug(i)
        # logging.debug(ary2)
        content = {
                    'type': 'text',
                    'text': ary1[i],
                    'color':'#4f6a8f',
                    'wrap':True,
                    'action':{
                        'type': 'postback',
                        'data': str(id-(len_max-i))
                        # ↓これだと一時したらずれてきます
                        # 'data': str(id-(len(ary1)-1-i))
                    }
                }
        contents.append(content)
        # if i >= 3:
        #     break
    data = {
        'replyToken': replyToken,
        'messages': [
            {
                "type": "flex",
                "altText": "料理を選んでください",
                "contents": {
                    "type": "bubble",
                    'body': {
                        'type': 'box',
                        'layout': 'vertical',
                        'contents': contents
                    }
                }
            }
        ]
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logging.debug(response)

# 料理を確定して、カロリーを返す
def res_cal(replyToken, name_result, cal_result):
    # db = Database()
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    data = {
        'replyToken': replyToken,
        'messages': [{
            'type': 'text',
            'text': f'{name_result}のカロリーは、{cal_result}kcalです'
        },{
            'type':'text',
            'text':'体重を入力してください！（小数点可）'
        }]
    }
    requests.post(url, data=json.dumps(data), headers=headers)

# カロリーと体重を受け取って、計算してリストに格納する
def calc(cal_result, weight,replyToken):
    motion = []
    cal_result = cal_result['cal']
    # try:
    #     weight = float(weight)
    #     if weight <= 0:
    #         res_weight(replyToken)
    # except ValueError:
    #     res_weight(replyToken)
    # except ZeroDivisionError:
    #     res_weight(replyToken)


    motion.append(math.floor(cal_result/1.05/weight/1.0*60))  # 瞑想
    motion.append(math.floor(cal_result/1.05/weight/1.5*60))  # デスクワーク
    motion.append(math.floor(cal_result/1.05/weight/4.0*60))  # 自転車
    motion.append(math.floor(cal_result/1.05/weight/7.0*60))  # ジョギング
    motion.append(math.floor(cal_result/1.05/weight/11.0*60))  # ランニング

    logging.debug(motion)
    logging.debug(cal_result)
    logging.debug(weight)

    return motion

# 運動量を返す
def res_motion(motion, replyToken,cal_result,weight):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    data = {
        'replyToken': replyToken,
        'messages': [{
            'type': 'text',
            'text': f'体重が{weight}kgの方が{cal_result["cal"]}kcal消費するには、、、',
        },{
            'type':'text',
            'text':f'瞑想を{motion[0]}分してください！\n\nデスクワークを\n{motion[1]}分してください！\n\n自転車を\n{motion[2]}分漕いでください！\n\nジョギングを\n{motion[3]}分してください！\n\nランニングを\n{motion[4]}分してください！\n\nもう一度調べるには料理名を入力してください',
        }],
    }
    requests.post(url, data=json.dumps(data), headers=headers)

def first_comment(replyToken):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    data = {
        'replyToken':replyToken,
        'messages': [{
            'type':'text',
            'text': '最近食べた料理を教えてください！\n\n料理と体重から、カロリーを消費するために必要な運動量をご紹介します！\n\n見つからない時は、キーワードを変えてみてください\n\n例）\nラーメン→味噌ラーメン\nかれーらいす→カレーライス'
        }]
    }
    requests.post(url, data=json.dumps(data), headers=headers)

# 体重入力時に例外が発生したら再入力を促す
def res_weight(replyToken):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    data = {
        'replyToken':replyToken,
        'messages': [{
            'type':'text',
            'text':'有効な数字を入力してください！'
        }]
    }
    requests.post(url, data=json.dumps(data), headers=headers)

#検索結果が０件の時の処理
def res_none(replyToken):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {H5eJQcpwwCTQO3WWQiJzwntbu1AlqilP8reYup5QdDyGjNp07+hgjEuIQltlL1eP1g5LdpNAxZkQwr4liCI8NY/jr9zl5MmihTrm8XvPoqahyCEk2RcY4zAQC+StDWO8C4ewOBPNgAxgdsO3lQRBLQdB04t89/1O/w1cDnyilFU=}'
    }
    data = {
        'replyToken':replyToken,
        'messages': [{
            'type':'text',
            'text':'何も見つかりませんでした、、、'
        },{
            'type':'text',
            'text':'ワードを変えてみてください！'
        }]
    }
    requests.post(url, data=json.dumps(data), headers=headers)