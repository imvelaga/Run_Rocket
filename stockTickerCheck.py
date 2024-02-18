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
cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where is_available = false and  serial_no > (SELECT serial_no FROM track_it.stock_master x WHERE ticker_name = 'AZXC') order by serial_no")
#cursor.execute("SELECT x.ticker_name FROM track_it.stock_master x where serial_no in(55000,16,55002,55003,55005,1656,54999,55001,55004,9) order by serial_no")
rows = cursor.fetchall()
for row in rows:        
    try:
        stock_info = yf.Ticker('TSLA')
        information = stock_info.info
        if 'symbol' in information and 'open' in information:  
            print(information)      
            shortName = information["shortName"] if 'shortName' in information else (None)
            industry = information["industry"] if 'industry' in information else (None)
            sector = information["sector"] if 'sector' in information else (None)
            region = information["region"] if 'region' in information else (None)
            cursor.execute("UPDATE track_it.stock_master SET short_name=%s, stock_industry=%s, stock_sector=%s, region=%s where ticker_name =%s",
            (shortName,industry,sector,region,row[0]))
            conn.commit()
            print(row[0] + ' Has Data')
        else:
            print('No Data '+row[0])
    except Exception as ex:
        print(ex)
        #send_email("Error: {}".format(str(ex))+ "From callStockDetailsAPI_4")
cursor.close()
conn.close()