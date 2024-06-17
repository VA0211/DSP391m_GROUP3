**Environment** 
- Create virtual environment then install required packages:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Selenium**
- Used to crawl data from 1/1/2018 to 27/1/2020
- Chrome version: 125.0.6422.61 (64bit) - 20/5/2024
- [Chromedriver](https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.60/win64/chromedriver-win64.zip)

**Error**
1. Data crawling:
- Not having data on vietcombank website - Drop:
    + 2019: 22/12
    + 2016: 18/7
    + 2015: 20,21/; 28/9
    + 2013: 22/4; 6/12
    + 2012: 10,17,24/6; 1,8,15,22/7
- Some old date (<=2020) have the wrong value: 11/10/2019, 29/11/2018, 5/7/2018, 24-25/4/2018 (They all have the value of 25.459k on Sell column) - Done fixing