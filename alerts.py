import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os.path
import time

def enviar_email(file_location):
    email = ''
    password = ''
    subject = 'This is the subject'
    message = 'This is my message'
    #file_location = 'screenshot/ScreenShot1.png'

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb").read()
    image = MIMEImage(attachment, name=filename)
    msg.attach(image)

    
    f = open("log.txt")
    attachment = MIMEText(f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename="log.txt") 
    
    msg.attach(attachment)


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, email, text)
    server.quit()