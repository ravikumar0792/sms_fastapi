import smtplib
from email.mime.text import MIMEText
from app.core.config import settings


def send_verification_email(to_email: str, token: str):
    verify_link = f"{settings.FRONTEND_URL}/auth/verify?token={token}"

    subject = "Verify Your Email"
    body = f"""
    Hi,

    Click the link below to verify your email:

    {verify_link}

    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.send_message(msg)


def send_reset_email(to_email: str, token: str):
    reset_link = f"http://localhost:8000/docs#/Auth/reset_password_auth_reset_password_post?token={token}"

    subject = "Reset Your Password"
    body = f"""
    Click the link below to reset your password:

    {reset_link}

    This link expires in 15 minutes.
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.send_message(msg)