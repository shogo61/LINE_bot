import requests
from bs4 import BeautifulSoup
from database import Database  
import logging

class Search:

    def __init__(self) -> None:
        pass

    def Search(self, body_catch, replyToken):
        soup = BeautifulSoup(requests.get('https://calorie.slism.jp/?searchWord='+body_catch+'&search=検索').text,"html.parser")
        
        insert = Database()
        # logging.debug(soup)
        soup1 = soup.select('.searchName')
        soup2 = soup.select('.searchKcal')
        # logging.debug(soup1)
        for i in range(1,50,1):
            ary =[]
            ary.append(i)
            ary.append(replyToken)
            ary.append(soup1[i].text)
            ary.append(int(soup2[i].text))
            insert.Insert(ary)
            logging.debug(ary)

            ary.clear()
            
        