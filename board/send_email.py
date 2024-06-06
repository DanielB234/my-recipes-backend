import smtplib
from email.message import EmailMessage
import ssl
import os


SENDER_EMAIL = os.environ.get("SENDER_EMAIL")  # Sender email account 
PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Sender remote password
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL") # Email you want to receive Pdfs

def send_email(filename):
    message = EmailMessage()
    message["Subject"] = "My Recipes"
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    with open(filename, 'rb') as f:
        file_data = f.read()
    # Attach the PDF
    message.add_attachment(file_data, maintype='application', subtype='pdf', filename=filename)


    context = ssl.create_default_context() # Send the email
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(SENDER_EMAIL, PASSWORD)
        smtp.sendmail(SENDER_EMAIL,  RECEIVER_EMAIL, message.as_string())
    
    if os.path.exists(filename):
        os.remove(filename) # Delete the PDF from the file system now that it is sent