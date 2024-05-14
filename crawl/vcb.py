import requests
from bs4 import BeautifulSoup
import pandas as pd

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

def main():
    # date = input("Enter date (dd/mm/yyyy): ")
    date = '07/05/2024'
    exchange_rates = get_exchange_rate_by_day(date)
    if exchange_rates is not None:
        exchange_rates.to_csv('crawl/data/vcb_rates.csv', index=False, header=True)
    else:
        print("Exchange rates not found for the given date")

if __name__ == "__main__":
    main()
