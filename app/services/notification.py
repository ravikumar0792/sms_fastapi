import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
from fastapi import BackgroundTasks

def send_email(to_email: str, subject: str, body: str):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.sendmail(settings.SMTP_FROM, [to_email], msg.as_string())

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Email failed: {e}")

def send_sms(phone: str, message: str):
    try:
        # Placeholder (Twilio later)
        print(f"📱 SMS sent to {phone}: {message}")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

def send_email_background(background_tasks: BackgroundTasks, to_email, subject, body):
    background_tasks.add_task(send_email, to_email, subject, body)