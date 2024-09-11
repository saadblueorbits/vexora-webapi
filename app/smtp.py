# Function to send an email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from app.config import settings


def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = settings.SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body with MIMEText
    msg.attach(MIMEText(body, 'plain'))

    # Send the email via SMTP server
    try:
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")