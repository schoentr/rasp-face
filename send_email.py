import os
from os.path import join, dirname
from dotenv import load_dotenv
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# load sender email and password and recipient password from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Define to/from email addresses and subject information
from_addr = os.environ.get('FROM_ADDR')
password = os.environ.get('FROM_PASSWORD')
to_addr = os.environ.get('TO_ADDR')

subject = 'SnakeEyes Notification'

# Create multi-part email instance and add pre-defined variables
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

# attach the text of the body of the email
body = 'Unknown face detected -- see attachment.'
msg.attach(MIMEText(body, 'plain'))

# include an attachment to the email
file_name = './test_assets/kaja.mp4'
attachment = open(file_name, 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= " + file_name)
msg.attach(part)

# open gmail server and login as sender
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(from_addr, password)

# send the email
text = msg.as_string()
server.sendmail(from_addr, to_addr, text)

# close the server
server.quit()
