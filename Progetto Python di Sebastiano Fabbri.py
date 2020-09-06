import requests
import json
import schedule
import time
from datetime import date
from pprint import pprint
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

params = {
    'start': '1',
    'limit': '100',
    'convert': 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'b3f2a8b5-8330-4853-8b1b-e8f2f184c217'
}

data = requests.get(url=url, headers=headers, params=params).json()
pprint(data)

r = requests.get(url=url, headers=headers, params=params).json()

def daily_Report():
    final_data = []

    #La criptovaluta con il volume maggiore (in $) delle ultime 24 ore
    vol = []
    sym = []

    for field in r['data']:
        vol.append(
            field['quote']['USD']['volume_24h']
       )

    maxvol = max(float(value) for value in vol)

    for field in r['data']:
        if maxvol == field['quote']['USD']['volume_24h']:
            sym.append(
                field['symbol']
            )

    titolo1 = "Cripto vol maggiore"
    final_data.append(titolo1)
    final_data.append(sym)
    final_data.append(maxvol)

    #Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
    percent_24h = []
    sym_migliori = []
    sym_peggiori = []

    for field in r['data']:
        percent_24h.append(
            field['quote']['USD']['percent_change_24h']
        )
    percent_24h.sort(reverse=True)
    migliori_10 = percent_24h[:10]
    peggiori_10 = percent_24h[-10:]
    peggiori_10.sort()

    for val in migliori_10:
        for field in r['data']:
            if val == field['quote']['USD']['percent_change_24h']:
                sym_migliori.append(
                    field['symbol']
                )

    for val in peggiori_10:
        for field in r['data']:
            if val == field['quote']['USD']['percent_change_24h']:
                sym_peggiori.append(
                    field['symbol']
                )

    titolo2 = "migliori10"
    final_data.append(titolo2)
    for sym, best10 in zip(sym_migliori, migliori_10):
        best_cripto_percent_24h = (sym,best10)
        final_data.append(best_cripto_percent_24h)

    titolo2bis = "peggiori10"
    final_data.append(titolo2bis)
    for sym, last10 in zip(sym_peggiori, peggiori_10):
        last_cripto_percent_24h = (sym,last10)
        final_data.append(last_cripto_percent_24h)

    #La quantità di denaro necessaria per acquistare una unità di ciascuna delle prime 20 criptovalute (secondo classifica coinmarketcap)
    money_cripto = []

    for field in r['data']:
        money_cripto.append(
            field['quote']['USD']['price']
        )

    first20 = money_cripto[:20]
    somma_first20 = sum(first20)
    titolo3 = "denaro necessario comprare 1unit prime 20 cripto"
    final_data.append(titolo3)
    final_data.append(somma_first20)

    #La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
    price_cripto = []

    titolo4 = "Money need to buy 1unit cripto vol > 76mln"
    final_data.append(titolo4)
    for field in r['data']:
        if field['quote']['USD']['volume_24h'] > 76000000:
            price_cripto.append(
                field['quote']['USD']['price']
            )
    s_price_cripto = sum(price_cripto)
    final_data.append(s_price_cripto)

    #La percentuale di guadagno o perdita che avreste realizzato se aveste comprato una unità di ciascuna delle prime 20 criptovalute* il giorno prima (ipotizzando che la classifca non sia cambiata)
    prezzo_cripto = []
    first20price = []
    percent24h = []

    for field in r['data']:
        prezzo_cripto.append(
            field['quote']['USD']['price']
        )

    first20price = prezzo_cripto[:20]

    for field in r['data']:
        percent24h.append(
            field['quote']['USD']['percent_change_24h']
        )

    first20percent24h = percent24h[:20]

    price100 = [x * 100 for x in(first20price)]

    sum_percent = [x + 100 for x in(first20percent24h)]

    price_yesterday = [x / y for x, y in zip(price100, sum_percent)]

    somma_price = sum(first20price)
    somma_y_price = sum(price_yesterday)

    final_percent = ((int(somma_price) / int(somma_y_price)) * 100) - 100

    titolo5 = "Valore all'acquisto 24h precedenti"
    final_data.append(titolo5)
    final_data.append(somma_y_price)
    titolo5bis = "Valore all'acquisto oggi"
    final_data.append(titolo5bis)
    final_data.append(somma_price)
    titolo5tris = "Variazione percentuale"
    final_data.append(titolo5tris)
    final_data.append(final_percent)

    def get_filename_datetime():
        return "Report " + str(date.today()) + ".json"
    name = get_filename_datetime()

    with open(name,'w') as file:
        json.dump(final_data, file)

schedule.every().day.at("12:00").do(daily_Report)

while 1:
    schedule.run_pending()
    time.sleep(1)