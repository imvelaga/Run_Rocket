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

serial_from= 1
serial_to = 480000
cookie = None
crumb = None
try:
    def get_yahoo_cookie():
        #cookie = None

        user_agent_key = "User-Agent"
        user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        headers = {user_agent_key: user_agent_value}
        response = requests.get(
            "https://fc.yahoo.com", headers=headers, allow_redirects=True
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
#cursor.execute("SELECT x.* FROM track_it.stock_master x where serial_no = 364677 order by serial_no")
cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where is_available = true and serial_no between %s and %s order by serial_no", (serial_from,serial_to))
rows = cursor.fetchall()
for row in rows:
        try:
            stock_info =  json.loads(get_stock_details(crumb,cookie,row[0]))
            if len(stock_info["quoteResponse"]["result"]) > 0:
                information = stock_info["quoteResponse"]["result"][0]
                if 'symbol' in information and 'regularMarketPrice' in information:        
                    shortName = information["shortName"] if 'shortName' in information else (None)
                    region = information["region"] if 'region' in information else (None)
                    cursor.execute("UPDATE track_it.stock_master SET region=%s where ticker_name =%s",
                    (region,row[0]))
                    conn.commit()
                    print(row[0] + ' Has Stock')
                else:
                    print('No Stock '+row[0])
                    cursor.execute("UPDATE track_it.stock_master SET is_available=%s where ticker_name =%s",
                    ("false",row[0]))
        except Exception as ex:
            print(ex)
            #send_email("Error: {}".format(str(ex))+ "From callStockDetailsAPI_4")
cursor.close()
conn.close()