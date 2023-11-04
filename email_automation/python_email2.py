import os
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
PORT = 587 # see why using port 587 is better than 465, with TLS and how to modify the script here
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')

subject = 'Second automated email'
# body = 'Please see the attached document'
receiver_email = 'r.a.finkel7@gmail.com'

message = MIMEMultipart('alternative') # instantiating the MIMEMultipart object/takes care of to, from and subject
message['From'] = EMAIL
message['To'] = receiver_email
message['Subject'] = subject

# message.attach(MIMEText(body, 'plain'))  # MIMEText takes care of the emails body

filename = 'Bookings Data.xlsx'
filename2 = 'index.html'

text = """\
Hi there,

Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.

This is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.

Good luck! Hope it works.
"""

with open(filename2, 'r') as file:
    html = file.read()
    
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

message.attach(part1)
message.attach(part2)

with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet_stream') # instantiate the MIMEBase object for the attachment
    part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header(
    'Content-Disposition',
    f"attachment; filename = {filename}",
)

message.attach(part)  # attaches the document to the message object
text = message.as_string()

context = ssl.create_default_context()
# with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
#     server.login(EMAIL, PASSWORD)
#     server.sendmail(EMAIL, receiver_email, text)

with smtplib.SMTP(SMTP_SERVER, PORT) as server:
    server.starttls(context=context)
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, receiver_email, text)