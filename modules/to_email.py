import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
from dotenv import load_dotenv


# send email
def send_email(email_recipient, email_subject, email_message, attachment_location = []):
    
    load_dotenv("./.env")
    EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
     
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = email_recipient
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_message, "plain"))
    
    if len(attachment_location) > 0:
        for att in attachment_location:
            filename = os.path.basename(att)
            attachment = open(att, "rb")
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", 
                            "attachment; filename= %s" % filename)
            msg.attach(part)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, email_recipient, text)
        server.quit()
    except:
        print("SMPT server connection error")
        return False
    
    return True
