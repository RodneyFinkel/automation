import logging
import os
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s", level=logging.INFO
)

SMTP_SERVER = os.environ.get('SMTP_SERVER')
PORT = os.environ.get('EMAIL_PORT')
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

def send_email(to_email: str, subject: str, attachment_name: str):
    # Assumes SMTP server requires TLS encryption
    message = MIMEMultipart()
    message['From'] = EMAIL
    message['To'] = to_email
    message['Subject'] = subject
    body = 'Hi there\n\nPlease find your report attached.\n\nThanks'
    
    message.attach(MIMEText(body, 'plain'))
    
    with open(attachment_name, 'rb') as file:
        part = MIMEBase(
            'application',
            'octet_stream',
            # 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'   
        )
        # part is a MIMEBase object initialized to have the data the context manager has opened read into it by the set_payload method
        part.set_payload(file.read()) # loads the file's binary content into the attachment object
        
    encoders.encode_base64(part)  # encodes the binary data into ASCII text
    
    part.add_header(
        'Content-Disposition',
        f"attachment: filename = {attachment_name}",
    )
    
    logging.info(f"Attaching {attachment_name} to the email")
    message.attach(part)  # attach() method is from the MIMEMultipart class used earlier to initialize the message object. Here is attaches an object from the MIMEBase class (part) to the MIMEMultipart object, message
    text = message.as_string() # as_string() method also belongs to MIMEMultipart class that can operate on the MIMEMultipart object, message
    
    context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
    #     logging.info(f"Sending email to {to_email}")
    #     server.login(EMAIL, PASSWORD)
    #     server.sendmail(EMAIL, receiver_email, text)
    
    
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        logging.info(f"Sending email to {to_email}")
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, text)
        logging.info(f"Succesfully sent email to {to_email}")