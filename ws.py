import requests
import csv
import os
import pandas

from bs4 import BeautifulSoup
from datetime import datetime

def formatNumber(numb):
    n = ''.join(c for c in numb if c.isdigit() or c == ',')
    if(n == ''):
        n = 0
    else: 
        n = n.replace(',','.')
        n = float(n)
    return n

dates = []
names = []
cPrices = []
tPrices = []

todayDate = datetime.today().strftime('%d-%m-%Y')
contadorPaginas = 1

strPage = "https://store.steampowered.com/search/?page="

page = requests.get(strPage)
soup = BeautifulSoup(page.content, features="lxml")
div = soup.find('div', attrs={'class':'search_pagination_right'})
children = div.findChildren("a" , recursive=False)
lastPage = int(children[2].text)

while(contadorPaginas <= lastPage):
    page = requests.get(strPage+str(contadorPaginas))
    soup = BeautifulSoup(page.content, features="lxml")
    resultsRows = soup.find(id="search_resultsRows")

    if(resultsRows == None):
        for i in range(0,10) and resultsRows == None:
            page = requests.get(strPage+str(contadorPaginas))
            soup = BeautifulSoup(page.content, features="lxml")
            resultsRows = soup.find(id="search_resultsRows")

        if(resultsRows == None):
            continue

    resultsA = resultsRows.findAll('a')
    for a in resultsA:
        title = a.find('span', attrs={'class':'title'}).text
        price = a.find('div', attrs={'class':'col search_price responsive_secondrow'})
        cprice = 0

        #El juego no está rebajado o es gratis
        if(price != None):
            price = formatNumber(price.text.strip())
            cprice = price
        #Juego rebajado
        else:
            price = a.find('div', attrs={'class':'col search_price discounted responsive_secondrow'}).text.strip()
            pricesL = price[:-1].split("€")
            price = formatNumber(pricesL[0])
            cprice = formatNumber(pricesL[1])
        
        dates.append(todayDate)
        names.append("\'"+title+"\'")
        cPrices.append(cprice)
        tPrices.append(price)

    print(str(contadorPaginas) + ' de '+str(lastPage))
    contadorPaginas += 1
    
df = pandas.DataFrame(data={"Date": dates, "Name": names, "Total price": tPrices, "Current price": cPrices})
#df.to_csv("./file.csv", sep=',',index=False)

if not os.path.isfile("filename.csv"):
    df.to_csv("filename.csv", sep=',',index=False)
else:
    df.to_csv("filename.csv", mode='a', header=False)