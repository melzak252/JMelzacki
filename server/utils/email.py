

import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail

load_dotenv()

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
NOREPLY_EMAIL = os.getenv("NOREPLY_EMAIL")

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USERNAME,
    MAIL_PASSWORD=EMAIL_PASSWORD,  # Use the app password here
    MAIL_FROM=EMAIL_USERNAME,
    MAIL_PORT=465,
    MAIL_SERVER="mail.privateemail.com",
    MAIL_STARTTLS=False,  # Use False if you're using SSL/TLS on port 465
    MAIL_SSL_TLS=True,  # Enable SSL/TLS connection (True if you're using port 465)
    USE_CREDENTIALS=True,  # Use SMTP credentials
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path('templates')
)


conf_noreply = ConnectionConfig(
    MAIL_USERNAME=EMAIL_USERNAME,
    MAIL_PASSWORD=EMAIL_PASSWORD,  # Use the app password here
    MAIL_FROM=NOREPLY_EMAIL,
    MAIL_PORT=465,
    MAIL_SERVER="mail.privateemail.com",
    MAIL_STARTTLS=False,  # Use False if you're using SSL/TLS on port 465
    MAIL_SSL_TLS=True,  # Enable SSL/TLS connection (True if you're using port 465)
    USE_CREDENTIALS=True,  # Use SMTP credentials
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path('templates')
)

fm = FastMail(conf)
fm_noreply = FastMail(conf_noreply)