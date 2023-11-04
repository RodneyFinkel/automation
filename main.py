from data_automation import DataExporter
from mailer import send_email
from datetime import datetime
import schedule # for cron job

# 2 timestamp objects
start_timestamp = datetime(2023, 5, 28, 00, 00, 00)  # May 28 2023 00:00:00
end_timestamp = datetime(2023, 8, 20, 23, 59, 59)  # Aug 20 2023 23:59:59

# initialize DataExporter object
exporter = DataExporter()
# class method, .generate_excelsheet() from DataExporter returns either True or False
if exporter.generate_excelsheet(start_timestamp, end_timestamp, sheet_name='Bookings Data.xlsx'):
    send_email('r.a.finkel7@gmail.com', 'Your Report', 'Bookings Data.xlsx' )
    
    
def main():
    today = datetime.now()
    sheet_name = 'Bookings Data.xlsx'
    
    if today.weekday()==5: # 0 means Monday
        start_timestamp = (today - timedelta(days=7).replace(hour=0, minute=0, second=0, microsecond=0))
        end_timestamp = (today - timedelta(days=1).replace(hour=23, minute=59, second=59, microsecond=0))
        sheet_name = 'Weekly Report.xlsx'
    elif today.day == 29:
        start_timestamp = (today.replace(day=1) - timedelta(days=1)
                           ).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_timestamp = (today.replace(day=1) - timedelta(days=1)
                         ).replace(hour=23, minute=59, second=59, microsecond=0)
        sheet_name = "Monthly Report.xlsx"
        
    exporter = DataExporter()
    exporter.generate_excelsheet(
        start_timestamp, end_timestamp, sheet_name
    )
    
    send_email('r.a.finkel7@gmail.com',
               'Your Report', sheet_name)
    
schedule.every().day.at('08:00').do(main)

while True:
    schedule.run_pending()        
        
       