import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')
PORT = 465

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', PORT, context=context) as server:
    # server.starttls(context=context) # secure the connection
    server.login(EMAIL, PASSWORD)
    message = """\
        Subject: Automated Email
        
        Body: Hello there, this is an automated email sent using python. 
        But i would just like to know where the hell my cat is???
        """
        
    server.sendmail(
        EMAIL,
        'r.a.finkel7@gmail.com',
        message
         )




