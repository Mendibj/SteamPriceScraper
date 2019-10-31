import requests
import csv
import os
import pandas
import time
import argparse
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

def getLastPage(strPage):
    page = requests.get(strPage)
    soup = BeautifulSoup(page.content, features="lxml")
    div = soup.find('div', attrs={'class':'search_pagination_right'})
    children = div.findChildren("a" , recursive=False)
    return int(children[2].text)

parser = argparse.ArgumentParser()
parser.add_argument("--fp", help="Page where starts the scraping")
parser.add_argument("--lp", help="Page where ends the scraping")
args = parser.parse_args()

dates = []
names = []
cPrices = []
tPrices = []

strPage = "https://store.steampowered.com/search/?page="
logError = open("Logs_error.txt","a",encoding='utf-8')

contadorPaginas = int(args.fp) if args.fp != None else 1
lastPage = int(args.lp) if args.lp != None else getLastPage(strPage)

while(contadorPaginas <= lastPage):
    page = requests.get(strPage+str(contadorPaginas))
    intentos = 0
    soup = BeautifulSoup(page.content, features="lxml")
    resultsRows = soup.find(id="search_resultsRows")

    while(resultsRows == None and intentos < 10):
        time.sleep(5)
        soup = BeautifulSoup(page.content, features="lxml")
        resultsRows = soup.find(id="search_resultsRows")
        intentos += 1

    if(resultsRows == None):
        logError.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+' Error al cargar la página '+str(contadorPaginas)+'\n')
    else:
        resultsA = resultsRows.findAll('a')
        for a in resultsA:
            try:
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

                dates.append(datetime.today().strftime('%d-%m-%Y %H:%M'))
                names.append("\'"+title+"\'")
                cPrices.append(cprice)
                tPrices.append(price)
            except:
                logError.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+' Error al cargar la página '+str(contadorPaginas)+'\n')

    print(str(contadorPaginas) + ' de '+str(lastPage))
    contadorPaginas += 1
    
df = pandas.DataFrame(data={"Date": dates, "Name": names, "Total price": tPrices, "Current price": cPrices})

csvName = "data.csv"
if not os.path.isfile(csvName):
    df.to_csv(csvName, sep=',',index=False)
else:
    df.to_csv(csvName, mode='a', header=False)
logError.close()
