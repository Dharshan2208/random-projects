import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_summary_email(summary_text):
    sender = EMAIL_USER
    recipient = os.getenv("EMAIL_TO")
    password = EMAIL_PASS

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Baka --> Here's Your Unread Email Summary......Do Read It...Baka Yaro.."

    formatted_text = f"\nYour Unread Email Summaries\n\n{summary_text}\n\nRegards,\nYour One and Only Baka Bot....Peace Bro"
    message.attach(MIMEText(formatted_text, "plain"))

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())
        server.quit()
        print("Summary sent to your inbox.")
    except Exception as e:
        print(f"Failed to send email summary: {str(e)}")
