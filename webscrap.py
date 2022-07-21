from flask import Flask,request,jsonify
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen, urlretrieve, Request
from urllib.error import URLError, HTTPError


app = Flask(__name__)

url = 'https://www.hltv.org/stats/players?startDate=all'
headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
req = Request(url,headers=headers)
response = urlopen(req)
html = response.read()
soup = BeautifulSoup(html,'html.parser')




numPlayers = soup.findAll('td',class_='playerCol')
numPlayers1 = range(int(len(numPlayers)))

nomePlayers = soup.find('td',class_='playerCol').getText()
nacionalidade = soup.find_all('td', attrs={'class': 'teamCol'})
mapasJogados = soup.find('td',class_='statsDetail').getText()
rounds = soup.find('td',class_='statsDetail gtSmartphone-only').getText()
killDeathDiff = soup.find('td',class_='kdDiffCol won').getText()
rating = soup.find('td',class_='ratingCol').getText()

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
    try:
        kdiff.append(int(c.text[1:]))
    except:
        kdiff.append('sem info')


time = []
for lista in soup.find_all('td', attrs={'class': 'teamCol'}):
    timePlayer = lista.find("img")['title']
    time.append(timePlayer)

rating = []
for lista in soup.find_all('td', attrs={'class': 'ratingCol'}):
    ratingPlayer = float(lista.text)
    rating.append(ratingPlayer)

times_anteriores = []

modelo = soup.find_all('span' , attrs='gtSmartphone-only')

for lista in range(0, len(players)):
    lista_times = []
    for c in modelo[lista]:
        try:
            lista_times.append(c.find("img")['title'])
        except:
            pass
    times_anteriores.append(lista_times)

main_df = pd.DataFrame(list(zip(nacionalidades,players,time,maps,status,kdiff,KD,rating)),columns=[['Nacionalidade', 'Jogadores', 'Time', 'Maps', 'Rounds', 'KDiff', 'KD', 'Rating']])



jogadores = []
for c in range(0,len(players)):
    dicionario = {}
    dicionario['id'] = players[c].lower()
    dicionario['nacionalidade'] = nacionalidades[c]
    dicionario['time'] = time[c]
    dicionario['times_anteriores'] = times_anteriores[c]
    dicionario['maps'] = maps[c]
    dicionario['rounds'] = status[c]
    dicionario['kdiff'] = kdiff[c]
    dicionario['kd'] = KD[c]
    dicionario['rating'] = rating[c]
    jogadores.append(dicionario)



@app.route('/jogadores/<id>/',methods=['GET'])
def players(id):
    for index in range(0,len(jogadores)):
        if jogadores[index]['id'] == id:
            response = jogadores[index]
            return response

if __name__ == "__main__":
    app.run(debug=True)
