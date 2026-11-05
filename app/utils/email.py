import logging
import smtplib
from email.message import EmailMessage
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from app.core.config import settings

BASE_DIR: Path = Path(__file__).resolve().parent.parent

template_env: Environment = Environment(loader=FileSystemLoader(BASE_DIR / "templates"))

logger: logging.Logger = logging.getLogger(__name__)


def load_email_template(template_name: str, context: dict[str, str]) -> str:
    template: Template = template_env.get_template(template_name)
    return template.render(context)


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str = "Please view this email in an HTML-compatible email client.",
) -> None:
    try:
        message: EmailMessage = EmailMessage()

        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = to_email
        message["Subject"] = subject

        # Plain-text fallback
        message.set_content(text_content)

        # HTML email content
        message.add_alternative(html_content, subtype="html")

        server: smtplib.SMTP
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )
            server.send_message(message)

    except Exception:
        logger.exception("Failed to send email to %s", to_email)


def send_complaint_registered_email(
    customer_email: str,
    complaint_number: str,
) -> None:
    html_content: str = load_email_template(
        "complaint_registered.html",
        {
            "complaint_number": complaint_number,
        },
    )

    send_email(
        to_email=customer_email,
        subject="EB Complaint Registered Successfully",
        html_content=html_content,
        text_content=(
            f"Your complaint {complaint_number} "
            "has been registered successfully. Current status: PENDING."
        ),
    )


def send_complaint_closed_email(
    customer_email: str,
    complaint_number: str,
) -> None:
    html_content: str = load_email_template(
        "complaint_closed.html",
        {
            "complaint_number": complaint_number,
        },
    )

    send_email(
        to_email=customer_email,
        subject="EB Complaint Closed Successfully",
        html_content=html_content,
        text_content=(
            f"Your complaint {complaint_number} "
            "has been repaired and closed successfully. "
            "Current status: CLOSED."
        ),
    )
