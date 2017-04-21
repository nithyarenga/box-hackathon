import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import email_config as email_value

def send_email(fromaddr, toaddr, subject, body):
   try:
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.ehlo()
   except:
       print('Something went wrong...')
   #Next, log in to the server
   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = toaddr
   msg['Subject'] = subject
   msg.attach(MIMEText(body, 'plain'))
   server.ehlo()
   server.starttls()
   server.ehlo()
   server.login(email_value.username, email_value.password)
   text = msg.as_string()
   server.sendmail(fromaddr, toaddr, text)

