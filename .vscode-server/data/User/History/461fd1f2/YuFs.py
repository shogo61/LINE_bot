import requests
from bs4 import BeautifulSoup
import logging

class Search:

    # def __init__(self) -> None:
    #     pass

    # 料理名とカロリーをWebサイトから持ってきてaryに格納する
    def Search(self, body_catch):
        soup = BeautifulSoup(requests.get('https://calorie.slism.jp/?searchWord='+body_catch+'&search=検索').text,"html.parser")
        
        soup1 = soup.select('.searchName')
        soup2 = soup.select('.searchKcal')
        ary1 = []
        ary2 = []
        # for i in range(0,4,1):
        logging.debug(soup1)
        i = 0
        for i in range(len(soup1)):
            if body_catch in soup1[i].text:
                ary1.append(soup1[i].text)
                ary2.append(int(soup2[i].text))
                # i += 1
            if i >= 5:
                break
        # logging.debug(ary)
        return ary1,ary2

            
        