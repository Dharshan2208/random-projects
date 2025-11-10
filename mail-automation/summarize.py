import imaplib
import email
import time
from dotenv import load_dotenv
import os
from groq import summarize_with_groq
from clean_subject import clean_subject
from email_sender import send_summary_email
from gemini import classify_email


load_dotenv()
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def fetch_and_summarize_emails():
    try:
        #Connects to Gmail using SSL encryption and then logins it.
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")
        status, messages = mail.search(None, '(UNSEEN)')

        email_ids = messages[0].split()
        if not email_ids:
            print("No unread emails.")
            return

        summary_report = ""
        print(f"📥 Found {len(email_ids)} unread email(s).\n")

        for num in email_ids:
            #For looping through unread messages
            #RFC822 fetches the full raw content of the email.
            status, msg_data = mail.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = clean_subject(msg["subject"])
                    sender = msg.get("From")
                    body = ""

                    #This loop finds the plain text part (ignores attachments) and decode=True converts bytes to text.
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    summary = summarize_with_groq(body)
                    category = classify_email(subject, body)
                    summary_report += (
                        f"From: {sender}\n"
                        f"Subject: {subject}\n"
                        f"Category: {category}\n"
                        f"Summary:\n{summary}\n"
                        f"{'-'*60}\n"
                    )

                    time.sleep(6)   #TO avoid API limit max

        if summary_report:
            send_summary_email(summary_report)

        mail.logout()

    except Exception as e:
        print(f"Error: {str(e)}")
