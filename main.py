from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError
from fastapi import FastAPI
from function import getkey
from webscrap import webscrap



url = 'https://www.hltv.org/stats/players?startDate=2021-06-22&endDate=2022-06-22'
headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')
lista = soup.find('table')

res = webscrap(lista,soup)

player = getkey(res,'s1mple')
app = FastAPI()

@app.get('/')
def raiz():
    return player

