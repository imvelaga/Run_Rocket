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
            shortName = information["shortName"] if 'shortName' in information else (None)  
            address = information["address1"] if 'address1' in information else (None)
            city = information["city"] if 'city' in information else (None)            
            state = information["state"] if 'state' in information else (None)
            zip = information["zip"] if 'zip' in information else (None)
            country = information["country"] if 'country' in information else (None)
            phone =  information["phone"] if 'phone' in information else (None)
            website = information["website"] if 'website' in information else (None)
            industry = information["industry"] if 'industry' in information else (None)
            industryKey = information["industryKey"] if 'industryKey' in information else (None)
            industryDisp = information["industryDisp"] if 'industryDisp' in information else (None)
            sector = information["sector"] if 'sector' in information else (None)
            sectorKey = information["sectorKey"] if 'sectorKey' in information else (None)
            sectorDisp = information["sectorDisp"] if 'sectorDisp' in information else (None)
            longBusinessSummary = information["longBusinessSummary"] if 'longBusinessSummary' in information else (None)
            fullTimeEmployees = information["fullTimeEmployees"] if 'fullTimeEmployees' in information else (None)
            auditRisk = information["auditRisk"] if 'auditRisk' in information else (None)
            boardRisk = information["boardRisk"] if 'boardRisk' in information else (None)
            compensationRisk = information["compensationRisk"] if 'compensationRisk' in information else (None)
            shareHolderRightsRisk = information["shareHolderRightsRisk"] if 'shareHolderRightsRisk' in information else (None)
            overallRisk = information["overallRisk"] if 'overallRisk' in information else (None)
            governanceEpochDate = information["governanceEpochDateinformation"] if 'governanceEpochDateinformation' in information else (None)
            compensationAsOfEpochDate = information["compensationAsOfEpochDate"] if 'compensationAsOfEpochDate' in information else (None)
            maxAge = information["maxAge"] if 'maxAge' in information else (None)
            priceHint = information["priceHint"] if 'priceHint' in information else (None)            
            sql = "INSERT INTO track_it.stock_details_log ( ticker_serial_no, created_date, address, city, state, zip, country, phone, website, industry, industry_key, industry_disp, sector, sector_key, sector_disp, long_business_summary, full_time_employees, audit_risk, board_risk, compensation_risk, share_holder_rights_risk, overall_risk, governance_epoch_date, compensation_as_of_epoch_date, max_age, price_hint) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #"UPDATE track_it.stock_details_log SET short_name=%s, address=%s, city=%s, state=%s, zip=%s, country=%s, phone=%s, website=%s, industry=%s, industry_key=%s, industry_disp=%s, sector=%s, sector_key=%s, sector_disp=%s, long_business_summary=%s, full_time_employees=%s, audit_risk=%s, board_risk=%s, compensation_risk=%s, share_holder_rights_risk=%s, overall_risk=%s, governance_epoch_date=%s, compensation_as_of_epoch_date=%s, max_age=%s, price_hint=%s WHERE ticker_name=%s"
            cursor.execute(sql,( row[1],"now()",address, city, state, zip ,country, phone, website, industry,industryKey,industryDisp,sector,sectorKey,sectorDisp,longBusinessSummary,fullTimeEmployees,auditRisk,boardRisk,compensationRisk,shareHolderRightsRisk,overallRisk,governanceEpochDate,compensationAsOfEpochDate,maxAge,priceHint))
            conn.commit()
            print(row[0] + ' Has Data')
        else:
            print('No Data '+row[0])
    except Exception as ex:
        print(ex)
        #send_email("Error: {}".format(str(ex))+ "From callStockDetailsAPI_4")
cursor.close()
conn.close()