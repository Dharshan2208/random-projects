import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
from gemini import classify_email
import time

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def ensure_folder(mail, folder_name):
    """Creates the folder if it doesn't exist."""
    result, folders = mail.list()
    folder_exists = any(folder_name.lower() in f.decode().lower() for f in folders)
    if not folder_exists:
        mail.create(folder_name)

def fetch_and_classify_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")  # fetch unseen emails
    email_ids = messages[0].split()  # process emails

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(BODY.PEEK[])")   #Tell IMAP to read without making it seen
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg.get("From")
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                body = ""
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = ""

                label = classify_email(subject, body)
                time.sleep(5)
                folder = clean(label)

                ensure_folder(mail, folder)
                mail.copy(eid, folder)

    mail.logout()