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
cursor.execute("SELECT x.ticker_name,x.ticker_serial_no FROM track_it.stock_ticker_master x order by ticker_serial_no")
rows = cursor.fetchall()
for row in rows:        
    try:
        stock_info = yf.Ticker(row[0])
        information = stock_info.info
        if 'symbol' in information and 'shortName' in information:
            shortName = information["shortName"] if 'shortName' in information else (None)
            cursor.execute("UPDATE track_it.stock_ticker_master SET short_name=%s,updated_date=%s,is_available=%s where ticker_name =%s",(shortName,"now()","true",row[0]))
            conn.commit()
            print(row[0] + ' Has Data')
        else:
           print('No Stock '+row[0])
           cursor.execute("UPDATE track_it.stock_ticker_master SET is_available=%s where ticker_name =%s",("false",row[0]))
           conn.commit()
    except Exception as ex:
        print(ex)
        print("Error: {}".format(str(ex)))
        #send_email("Error: {}".format(str(ex))+ "XXXX")
cursor.close()
conn.close()