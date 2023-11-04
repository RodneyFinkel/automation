from data_automation import DataExporter
from mailer import send_email
from datetime import datetime


# 2 timestamp objects
start_timestamp = datetime(2023, 5, 28, 00, 00, 00)  # May 28 2023 00:00:00
end_timestamp = datetime(2023, 8, 20, 23, 59, 59)  # Aug 20 2023 23:59:59

# initialize DataExporter object
exporter = DataExporter()
# class method, .generate_excelsheet() from DataExporter returns either True or False
if exporter.generate_excelsheet(start_timestamp, end_timestamp, sheet_name='Bookings Data.xlsx'):
    send_email('r.a.finkel7@gmail.com', 'Your Report', 'Bookings Data.xlsx' )
    
    

       