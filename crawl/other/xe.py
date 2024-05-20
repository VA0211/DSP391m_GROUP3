import pandas as pd
import datetime
from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def crawl_data(start_date, end_date, currency='VND'):
    crawl_list = []
    for single_date in daterange(start_date, end_date):
        df_crawl = pd.read_html(f'https://www.xe.com/currencytables/?from={currency}&date={single_date.strftime("%Y-%m-%d")}')[0]
        df_crawl['Date'] = single_date.strftime("%Y-%m-%d")
        crawl_list.append(df_crawl)
    df = pd.concat(crawl_list)
    return df

# Set period with the starting and ending day
start_date = date(2024, 1, 1)
end_date = date(2024, 5, 7)

df_vnd = crawl_data(start_date, end_date)
df_vnd.to_csv('crawl/data/xe_rates.csv', index=False, header=True)