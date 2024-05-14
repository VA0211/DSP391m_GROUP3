import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import timedelta, date
from time import sleep

def get_exchange_rate_by_day(date):
    url = f"https://portal.vietcombank.com.vn/UserControls/TVPortal.TyGia/pListTyGia.aspx?txttungay={date}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'rateTable'})
        rows = table.find_all('tr', {'class': 'odd'})
        exchange_rates = []
        for row in rows:
            cells = row.find_all('td')
            currency_name = cells[0].get_text(strip=True)
            currency_code = cells[1].get_text(strip=True)
            buy_cash = cells[2].get_text(strip=True).replace(',', '')
            buy_transfer = cells[3].get_text(strip=True).replace(',', '')
            sell = cells[4].get_text(strip=True).replace(',', '')
            exchange_rates.append({
                'Date': date,
                'Currency Name': currency_name,
                'Currency Code': currency_code,
                'Buy Cash': buy_cash,
                'Buy Transfer': buy_transfer,
                'Sell': sell
            })
        return pd.DataFrame(exchange_rates)

    else:
        print("Failed to fetch exchange rate data")
        return None

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def crawl_data(start_date, end_date):
    crawl_list = []
    for single_date in daterange(start_date, end_date):
        print(f"getting data for date {single_date}")
        df_crawl = get_exchange_rate_by_day(single_date)
        crawl_list.append(df_crawl)
        sleep(1)
    df = pd.concat(crawl_list)
    return df

def main():
    start_date = date(2023, 1, 1)
    end_date = date(2024, 1, 1)

    df_vnd = crawl_data(start_date, end_date)
    if df_vnd is not None:
        df_vnd.to_csv('data/vcb/vcb_rates_2023.csv', index=False, header=True)
    else:
        print("Exchange rates not found for the given date")

if __name__ == "__main__":
    main()