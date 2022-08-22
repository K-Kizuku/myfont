from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib
import os

FROM_ADDRESS = os.environ.get("FROM_ADDRESS")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addr, body_msg.as_string())
    smtpobj.close()
