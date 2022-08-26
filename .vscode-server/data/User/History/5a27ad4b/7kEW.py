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
        for i in range(1,6,1):
            ary =[]
            ary.append(i)
            ary.append(replyToken)
            # elems1 = soup.select('.searchNameVal:nth-of-type('+str(i)+')')
            # logging.debug(elems1)
            # element = elems1[i]
            # logging.debug(element)
            # name = str(soup1[i])
            # logging.debug(soup1[i])
            ary.append(str(soup1[i]))
            logging.debug(type(soup1[i]))

            # ary.append(element)
            ary.append(soup2[i])
            # logging.debug(elems2[i])
            # insert.Insert(ary)
            # logging.debug(ary)

            # ary.clear()
        
            
            
        