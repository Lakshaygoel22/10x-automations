import smtplib
import os
from email.mime.text import MIMEText

def send_email_report(report_content, to_email):
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASS")
    if not user or not password or user == "your_email@gmail.com":
        print("Gmail credentials not set in environment.")
        return
    msg = MIMEText(report_content)
    msg['Subject'] = 'AI Analysis: Funny Reactions on LinkedIn Post'
    msg['From'] = user
    msg['To'] = to_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(user, password)
            server.send_message(msg)
        print("Email report sent successfully to " + to_email)
    except Exception as e:
        print("Failed to send email: " + str(e))
