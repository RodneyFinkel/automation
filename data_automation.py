import logging
import os
import psycopg2
import pandas as pd
from datetime import datetime

from booking_encapsulation import BookingInfo

logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(messages)s", level=logging.INFO
)

DB_CONFIG = {
    'host': os.environ.get('DB_HOSTNAME'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USERNAME'),
    'password': os.environ.get('DB_PASSWORD'),
}
      
class DataExporter:
    
    def __init__(self):
        """Initialize the DataExporter with the database configuration."""
        self.db_config = DB_CONFIG  # will use ** operator to unpack kwargs in a different function call
        
    
    def __connect_to_database(self):
        """private method"""
        try:
            self.conn = psycopg2.connect(**self.db_config) # connect() returns a connection object that is stored in self.conn attribute
            self.cursor = self.conn.cursor() # cursor() creates a cursor object used to query the db directly with SQL
            logging.info('Connected to the database')
            
        except Exception as e:
            logging.error(
                'Failed to connect to the database with error: %s', e
                )
            raise
            
            
    def __fetch_from_database(self, start_timestamp, end_timestamp):
        """ Private method: Fetch booking data from the db for a given time range """
        self.__connect_to_database()
        query = f"""
        SELECT COUNT(*) AS num_bookings, SUM(total_amount) AS total_amount
        FROM bookings.bookings
        WHERE book_date >= {int(start_timestamp.timestamp())*1000} 
        AND book_date <= {int(end_timestamp.timestamp())*1000}
        """
        
        logging.info(
            "Extracting booking data from database for start_timestamp=%s and end_timestamp=%s",
            start_timestamp,
            end_timestamp,
             
        )
        result = None
        try:
            self.cursor.execute(query)
            result = list(self.cursor.fetchone()) # fetches the most recent sql query, returns a single row as a tuple, with each ellement of the tuple corresponding to a column in the result
            result.append(
                f"{start_timestamp.strftime('%d %b %Y')} - {end_timestamp.strftime('%d %b %Y')}"
            )
            logging.info(
                'Succesfully extracted bookings data from database for start_timestamp=%s and end_timestamp%s',
                start_timestamp,
                end_timestamp,
            )
        except Exception as e:
            logging.error(
                'Error occured while extracting booking data from database: %s', e
            )
        return result
    
    
    def __convert_to_excelsheet(self, data: list, sheet_name: str):
        """ Private method """
        try:
            booking_info = BookingInfo(data)  # BookingInfo class encapsulates data list
            data = {
                "": ["Total Bookings", "Total Amount ($)"],
                booking_info.get_timestamp(): [
                    booking_info.get_total_bookings(),
                    booking_info.get_total_amount(),
                ],
            } # excel sheet structure where every key-value pair is an excel column
            
            logging.info('Converting the data into a Pandas DataFrame')
            df = pd.DataFrame(data)
            logging.info("Inserting the data into an excelsheet")
            
            # ExcelWriter context manager
            with pd.ExcelWriter(sheet_name, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            logging.info('Succesfully inserted data in excelsheet')
        except ValueError as e:
            logging.error('Error converting data into excelsheet: %s', e)
    
    
    def generate_excelsheet(self, start_timestamp: datetime, end_timestamp: datetime, sheet_name: str = 'Bookings Data.xlsx'):
        """_summary_
        Public method to generate the excelsheet with booking data for a specified time range

        Args:
            start_timestamp (datetime): _description_
            end_timestamp (datetime): _description_
            sheet_name (str, optional): _description_. Defaults to 'Booking Data.xlsx'.
        """
        data = self.__fetch_from_database(start_timestamp, end_timestamp)
        if data is not None:
            self.__convert_to_excelsheet(data, sheet_name)
            return True
        else:
            logging.error('No data to convert and generate excelsheet')
            return False
        
            
    
        
           
        
          
    
    