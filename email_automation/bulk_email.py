import csv
import os
import smtplib
import ssl
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
PORT = 587
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

context = ssl.create_default_context()

with smtplib.SMTP(SMTP_SERVER, PORT) as server:
    server.starttls(context=context)
    server.login(EMAIL, PASSWORD)
    
    with open('receivers.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        
        for name, email, designation, salary in reader:
            message = f"""\
                Subject: {name}, you're hired!

                Hi {name}

                Congratulations, you're hired for the role of {designation}. Your salary will be {salary}.

                Thanks
                HR    
                """
            
            server.sendmail(EMAIL, email, message)
            