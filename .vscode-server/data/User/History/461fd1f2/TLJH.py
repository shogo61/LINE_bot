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
        ary =[]
        # for i in range(0,4,1):
        i = 0
        while i < 4:
            if body_catch in soup1[i].text:
                ary.append(soup1[i].text)
                ary.append(int(soup2[i].text))
                i += 1
            logging.debug(ary)
        return ary

            
        