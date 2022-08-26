import requests
from bs4 import BeautifulSoup
from database import Database  
import logging

class Search:

    def __init__(self) -> None:
        pass

    def Search(self, body_catch):
        soup = BeautifulSoup(requests.get('https://calorie.slism.jp/?searchWord='+body_catch+'&search=検索').text,"html.parser")
        
        insert = Database()
        # logging.debug(soup)
        soup1 = soup.select('.searchName')
        soup2 = soup.select('.searchKcal')
        # logging.debug(soup1)
        ary =[]
        for i in range(0,4,1):
            # ary.append(i)
            ary.append(soup1[i*2].text)
            ary.append(int(soup2[i*2+1].text))
            # insert.Insert(ary)
            # logging.debug(ary)
            # ary.clear()
        return ary

            
        