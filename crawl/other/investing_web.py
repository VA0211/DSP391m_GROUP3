import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_exchange_rate(start_date, end_date):
    url = f"https://www.investing.com/currencies/usd-vnd-historical-data?start_date={start_date}&end_date={end_date}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'curr_table'})
        
        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                date = cols[0].text.strip()
                price = cols[1].text.strip()
                data.append((date, price))
            
            df = pd.DataFrame(data, columns=['Date', 'USD/VND'])
            df['Date'] = pd.to_datetime(df['Date'])
            df['USD/VND'] = df['USD/VND'].str.replace(',', '').astype(float)
            return df
        else:
            print("Failed to find exchange rate table on the page.")
    else:
        print("Failed to retrieve data from the URL.")

if __name__ == "__main__":
    start_date = "01/01/2018"
    end_date = "01/01/2024"
    exchange_rate_data = scrape_exchange_rate(start_date, end_date)
    
    if exchange_rate_data is not None:
        print("USD/VND exchange rate data from Investing.com:")
        print(exchange_rate_data)
    else:
        print("Failed to retrieve exchange rate data.")
