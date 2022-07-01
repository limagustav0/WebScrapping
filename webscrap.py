from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError
from fastapi import FastAPI
from function import getkey

url = 'https://www.hltv.org/stats/players?startDate=2021-06-22&endDate=2022-06-22'

headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')

lista = soup.find('table')


def webscrap(lista,soup):
    numPlayers = soup.findAll('td',class_='playerCol')
    numPlayers1 = range(int(len(numPlayers)))

    nacionalidades = []
    for lista in soup.find_all('td', attrs={'class': 'playerCol'}):
        nacaoPlayer = lista.find("img")['title']
        nacionalidades.append(nacaoPlayer)

    players = []
    for c in soup.find_all('td', attrs={'class': 'playerCol'}):
        players.append(c.text)

    status = []
    for c in soup.find_all('td', attrs={'class': 'statsDetail'}):
        try:
            status.append(int(c.text))
        except:
            status.append(float(c.text))

    KD=[]
    for c in status:
        if type(c) == float:
            KD.append(c)

    for c in KD:
        status.remove(c)

    multiplos = [num for num in range(0,len(status)) if num % 2 == 0]

    maps=[]
    for c in multiplos:
        maps.append(status[c])

    for c in maps:
        status.remove(c)

    kdiff = []
    for c in soup.find_all('td', attrs={'class': 'kdDiffCol'}):
        kdiff.append(c.text)

    pais = []
    for lista in soup.find_all('td', attrs={'class': 'playerCol'}):
        paisPlayer = lista.find("img")['title']
        pais.append(paisPlayer)

    time = []
    for lista in soup.find_all('td', attrs={'class': 'teamCol'}):
        timePlayer = lista.find("img")['title']
        time.append(timePlayer)

    rating = []
    for lista in soup.find_all('td', attrs={'class': 'ratingCol'}):
        ratingPlayer = lista.text
        rating.append(ratingPlayer)

    main_df = pd.DataFrame(list(zip(nacionalidades,players,pais,time,maps,status,kdiff,KD,rating)),columns=[['Nacionalidade', 'Jogadores', 'Pais', 'Time', 'Maps', 'Rounds', 'KDiff', 'KD', 'Rating']])

    dicionario = {}
    listadict = []
    for c in range(0,len(players)):
        dicionario = {}
        dicionario['nome'] = players[c]
        dicionario['nacionalidade'] = nacionalidades[c]
        dicionario['pais'] = pais[c]
        dicionario['time'] = time[c]
        dicionario['maps'] = maps[c]
        dicionario['rounds'] = status[c]
        dicionario['kdiff'] = kdiff[c]
        dicionario['kd'] = KD[c]
        dicionario['rating'] = rating[c]
        listadict.append(dicionario)

    return listadict



