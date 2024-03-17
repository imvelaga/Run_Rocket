import psycopg2
import yfinance as yf
from sendEmail import send_email

conn = psycopg2.connect(
    host = 'localhost',
    database='postgres',
    user='postgres',
    password='postgres'
)

cursor = conn.cursor()
#cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where is_available = false and  serial_no > (SELECT serial_no FROM track_it.stock_master x WHERE ticker_name = 'AZXC') order by serial_no")
cursor.execute("SELECT x.ticker_name,x.ticker_serial_no FROM track_it.stock_ticker_master x where is_available = true order by ticker_serial_no")
rows = cursor.fetchall()
for row in rows:        
    try:
        stock_info = yf.Ticker(row[0])
        information = stock_info.info
        if 'symbol' in information and 'shortName' in information:
            regularMarketPreviousClose = information["regularMarketPreviousClose"] if 'regularMarketPreviousClose' in information else (None)  
            regularMarketOpen = information["regularMarketOpen"] if 'regularMarketOpen' in information else (None)
            regularMarketDayLow = information["regularMarketDayLow"] if 'regularMarketDayLow' in information else (None)            
            regularMarketDayHigh = information["regularMarketDayHigh"] if 'regularMarketDayHigh' in information else (None)
            bid = information["bid"] if 'bid' in information else (None)
            ask = information["ask"] if 'ask' in information else (None)
            bidSize =  information["bidSize"] if 'bidSize' in information else (None)
            askSize = information["askSize"] if 'askSize' in information else (None)
            lastFiscalYearEnd = information["lastFiscalYearEnd"] if 'lastFiscalYearEnd' in information else (None)
            nextFiscalYearEnd = information["nextFiscalYearEnd"] if 'nextFiscalYearEnd' in information else (None)
            firstTradeDateEpochUtc = information["firstTradeDateEpochUtc"] if 'firstTradeDateEpochUtc' in information else (None)
            timeZoneFullName = information["timeZoneFullName"] if 'timeZoneFullName' in information else (None)
            timeZoneShortName = information["timeZoneShortName"] if 'timeZoneShortName' in information else (None)
            uuid = information["uuid"] if 'uuid' in information else (None)
            sql = "INSERT INTO track_it.stock_data (ticker_serial_no,regular_market_previous_close,regularmarketopen, regularmarketdaylow, regularmarketdayhigh, bid, ask, bid_size, ask_size, last_fiscal_year_end, next_fiscal_year_end,first_trade_date_epochutc,timezone_full_name,timezone_short_name, uuid, load_date)VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (row[1],regularMarketPreviousClose,regularMarketOpen, regularMarketDayLow, regularMarketDayHigh ,bid, ask, bidSize, askSize, lastFiscalYearEnd,nextFiscalYearEnd,firstTradeDateEpochUtc,timeZoneFullName,timeZoneShortName, uuid,"now()")
            cursor.execute(sql, data)
            conn.commit()
            print(row[0] + ' Has Data')
        else:
            print('No Data '+row[0])
    except Exception as ex:
        print(ex)
        print("Error: {}".format(str(ex)))
        #send_email("Error: {}".format(str(ex))+ "XXXX")
cursor.close()
conn.close()