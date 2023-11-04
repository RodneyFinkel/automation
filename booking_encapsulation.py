from decimal import Decimal


class BookingInfo:
    def __init__(self, data_list: list):
        """
        Initialize BookingInfo with data from the database.

        Args:
            data_list (list): A list containing booking data (total_bookings, total_amount, timestamp).

        Note:
            The total_amount is converted to a Decimal type.
            
        Double underscores to make the data attributes private.
        
        """
        self.__total_bookings, self.__total_amount, self.__timestamp = data_list
        self.__total_amount = Decimal(self.__total_amount) if self.__total_amount else Decimal(0)
    
    
    def __str__(self):
        """
        Return a string representation of BookingInfo.

        """
        return f"Total Bookings: {self.__total_bookings}, Total Amount: ${self.__total_amount}"


    def get_total_bookings(self):
        
        return self.__total_bookings


    def get_total_amount(self):
        
        return self.__total_amount


    def get_timestamp(self):
        
        return self.__timestamp  
        
        
        