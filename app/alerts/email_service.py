import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class EmailService:
    """
    Service responsible for sending HTML email notifications.
    """

    @staticmethod
    def send(subject, html):
        """
        Sends an HTML email.

        Parameters
        ----------
        subject : str
            Subject of the email.

        html : str
            HTML content of the email.
        """

        # -----------------------------------------
        # Read email credentials from environment
        # -----------------------------------------
        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_APP_PASSWORD")
        receiver = os.getenv("EMAIL_RECEIVER")

        # -----------------------------------------
        # Create a multipart email message
        # -----------------------------------------
        msg = MIMEMultipart()

        # Sender email address
        msg["From"] = sender

        # Receiver email address
        msg["To"] = receiver

        # Email subject
        msg["Subject"] = subject

        # Attach HTML content to email
        msg.attach(
            MIMEText(html, "html")
        )

        # -----------------------------------------
        # Connect to Gmail SMTP server
        # -----------------------------------------
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:

                # Upgrade connection to encrypted TLS
                server.starttls()

                # Authenticate sender account
                server.login(sender, password)

                # Send the email
                server.send_message(msg)

                print("✅ Email Sent Successfully")

        except Exception as e:

            # Print error if email sending fails
            print(f"❌ Email Error: {e}")