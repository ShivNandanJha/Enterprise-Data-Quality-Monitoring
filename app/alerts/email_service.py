import os

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


class EmailService:

    @staticmethod
    def send(subject, html):

        sender = os.getenv("EMAIL_ADDRESS")

        password = os.getenv("EMAIL_APP_PASSWORD")

        receiver = os.getenv("EMAIL_RECEIVER")

        msg = MIMEMultipart()

        msg["From"] = sender

        msg["To"] = receiver

        msg["Subject"] = subject

        msg.attach(

            MIMEText(html, "html")

        )

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
                print("✅ Email Sent Successfully")
        except Exception as e:
            print(f"❌ Email Error: {e}")