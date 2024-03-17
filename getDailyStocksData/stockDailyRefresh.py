from urllib import response
import requests
import sys
import psycopg2
import json
from sendEmail import send_email

conn = psycopg2.connect(
    host = 'localhost',
    database='postgres',
    user='postgres',
    password='postgres'
)

cookie = None
crumb = None
try:
    def get_yahoo_cookie():
        #cookie = None

        user_agent_key = "User-Agent"
        user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        headers = {user_agent_key: user_agent_value}
        response = requests.get(
            "https://www.nellisauction.com/", headers=headers, allow_redirects=True
        )

        if not response.cookies:
            raise Exception("Failed to obtain Yahoo auth cookie.")

        cookie = list(response.cookies)[0]

        return cookie


    def get_yahoo_crumb(cookie):
        #crumb = None

        user_agent_key = "User-Agent"
        user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        headers = {user_agent_key: user_agent_value}

        crumb_response = requests.get(
            "https://query1.finance.yahoo.com/v1/test/getcrumb",
            headers=headers,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
        )
        crumb = crumb_response.text

        if crumb is None:
            raise Exception("Failed to retrieve Yahoo crumb.")

        return crumb

    def get_stock_details(crumb,cookie,ticker_code):
        res = None
        user_agent_key = "User-Agent"
        user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        y_url = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+ticker_code+"&crumb="
        headers = {user_agent_key: user_agent_value}
        stock_response = requests.get(
            y_url + crumb,
            headers=headers,
            cookies={cookie.name: cookie.value},
            allow_redirects=True,
        )

        res = stock_response.text
    
        if res is None:
            raise Exception("Failed to retrieve Yahoo Response.")
        return res
except Exception as e:
    print("Error: {}".format(str(e)))
    sys.exit(1)
    
# Usage
if __name__ == "__main__":
    cookie = get_yahoo_cookie()
    crumb = get_yahoo_crumb(cookie)

    cursor = conn.cursor()
    #cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where is_available is true and serial_no > (select serial_no from track_it.stock_master where ticker_name = 'IWFG') order by serial_no")
    cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where is_available is true order by serial_no")
    rows = cursor.fetchall()
    for row in rows:
            try:
                stock_info =  json.loads(get_stock_details(crumb,cookie,row[0]))
                if len(stock_info["quoteResponse"]["result"]) > 0:
                    information = stock_info["quoteResponse"]["result"][0]
                    if 'symbol' in information and 'regularMarketPrice' in information:        
                        
                        tickerName = information["symbol"] if 'symbol' in information else (None)                    
                        region = information["region"] if 'region' in information else (None)                    
                        quoteType = information["quoteType"] if 'quoteType' in information else (None)                    
                        shortName = information["shortName"] if 'shortName' in information else (None)                    
                        regularMarketDayRange = information["regularMarketDayRange"] if 'regularMarketDayRange' in information else (None)                    
                        regularMarketPreviousClose = information["regularMarketPreviousClose"] if 'regularMarketPreviousClose' in information else (None)                    
                        fiftyTwoWeekRange = information["fiftyTwoWeekRange"] if 'fiftyTwoWeekRange' in information else (None)                    
                        fiftyTwoWeekLow = information["fiftyTwoWeekLow"] if 'fiftyTwoWeekLow' in information else (None)                    
                        fiftyTwoWeekHigh = information["fiftyTwoWeekHigh"] if 'fiftyTwoWeekHigh' in information else (None)                    
                        trailingAnnualDividendRate = information["trailingAnnualDividendRate"] if 'trailingAnnualDividendRate' in information else (None)                    
                        trailingPE = information["trailingPE"] if 'trailingPE' in information else (None)                    
                        dividendRate = information["dividendRate"] if 'dividendRate' in information else (None)                    
                        trailingAnnualDividendYield = information["trailingAnnualDividendYield"] if 'trailingAnnualDividendYield' in information else (None)                    
                        #dividendYield = information["dividendYield"] if 'dividendYield' in information else (None)                    
                        epsTrailingTwelveMonths = information["epsTrailingTwelveMonths"] if 'epsTrailingTwelveMonths' in information else (None)                    
                        epsForward = information["epsForward"] if 'epsForward' in information else (None)                    
                        epsCurrentYear = information["epsCurrentYear"] if 'epsCurrentYear' in information else (None)                    
                        priceEpsCurrentYear = information["priceEpsCurrentYear"] if 'priceEpsCurrentYear' in information else (None)                    
                        twoHundredDayAverageChangePercent = information["twoHundredDayAverageChangePercent"] if 'twoHundredDayAverageChangePercent' in information else (None)                    
                        marketCap = information["marketCap"] if 'marketCap' in information else (None)                    
                        forwardPE = information["forwardPE"] if 'forwardPE' in information else (None)                    
                        priceToBook = information["priceToBook"] if 'priceToBook' in information else (None)
                        cursor.execute("INSERT INTO track_it.stock(ticker_name, region, quote_type, short_name, regular_market_day_range, regular_market_prev_close, fifty_two_week_range, fifty_two_week_low, fifty_two_week_high, trailing_ann_dividend_rate, trailing_pe, dividend_rate, trailing_ann_dividend_yield, eps_trailing_twelve_months, eps_forward, eps_current_year, price_eps_current_year, two_hundred_day_ann_avg_change_percent, market_cap, forward_pe, price_to_book, load_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (tickerName,region,quoteType,shortName,regularMarketDayRange,regularMarketPreviousClose,fiftyTwoWeekRange,fiftyTwoWeekLow,fiftyTwoWeekHigh,trailingAnnualDividendRate,trailingPE,dividendRate,trailingAnnualDividendYield,epsTrailingTwelveMonths,epsForward,epsCurrentYear,priceEpsCurrentYear,twoHundredDayAverageChangePercent,marketCap,forwardPE,priceToBook,"now()"))
                        conn.commit()
                        print(row[0] + ' Stock Data Inserted')
                    else:
                        print('No Stock '+row[0])
            except Exception as ex:
                print(ex)
                send_email("Error: {}".format(str(ex))+ "From stock daily reresh " + row[0])
    send_email("Sucessfullt load completed!!!")
    cursor.close()
    conn.close()