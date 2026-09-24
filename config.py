import os

from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.getenv(
    "ANTHROPIC_API_KEY"
)


SMTP_SERVER = os.getenv(
    "SMTP_SERVER",
    "smtp.gmail.com"
)


SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)


EMAIL_USERNAME = os.getenv(
    "EMAIL_USERNAME"
)


EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)
