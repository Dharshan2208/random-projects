import os
import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

DB_FILE = "github.db"

def create_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS followers (
                    username TEXT,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

def get_followers():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/followers"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    followers = []
    page = 1
    while True:
        res = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if res.status_code != 200:
            print("GitHub API error:", res.json())
            break
        data = res.json()
        if not data:
            break
        followers.extend([u["login"] for u in data])
        page += 1
    return followers

def save_today_followers(followers):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = str(date.today())

    c.execute("DELETE FROM followers WHERE date=?", (today,))  # avoid duplicates
    c.executemany("INSERT INTO followers VALUES (?, ?)", [(f, today) for f in followers])

    conn.commit()
    conn.close()

def get_followers_by_date(target_date):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT username FROM followers WHERE date=?", (str(target_date),))

    users = [u[0] for u in c.fetchall()]
    conn.close()
    return set(users)

def send_email(subject, message):

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    create_db()
    today = date.today()
    yesterday = today - timedelta(days=1)

    print("Fetching followers...")
    today_followers = set(get_followers())
    save_today_followers(today_followers)

    yesterday_followers = get_followers_by_date(yesterday)

    if not yesterday_followers:
        print("No data from yesterday — first run or missing record.")
        return

    unfollowers = yesterday_followers - today_followers

    if unfollowers:
        msg = " The following users unfollowed you on GitHub:\n\n" + "\n".join(unfollowers)
        send_email("GitHub Unfollower Alert", msg)
        print(msg)
    else:
        print(" No one unfollowed you today.")

if __name__ == "__main__":
    main()
