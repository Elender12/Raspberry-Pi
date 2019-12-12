#!/usr/bin/python



from smtplib import SMTP

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart



msg = MIMEMultipart()

msg['From']    = 'crelena12@gmail.com'

msg['To']      = 'darkpjo@gmail.com'

msg['Subject'] = 'Message subject'

msg.attach (MIMEText ('Message body', 'plain'))



smtp = SMTP()

smtp.connect ('smtp.gmail.com', 587)

smtp.sendmail (msg['From'], msg['To'], msg.as_string())

smtp.quit()