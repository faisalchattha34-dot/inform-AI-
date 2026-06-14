# email_service.py

import smtplib
import streamlit as st

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_form_email(
    receiver_email,
    form_name,
    form_link
):

    sender_email = st.secrets["EMAIL_ADDRESS"]
    sender_password = st.secrets["EMAIL_PASSWORD"]

    subject = f"Invitation: {form_name}"

    body = f"""
Hello,

You have been invited to complete the form:

{form_name}

Open the form using the link below:

{form_link}

Thank You.
"""

    try:
        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(
                body,
                "plain"
            )
        )

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:
        print(e)
        return False


def send_bulk_emails(
    email_list,
    form_name,
    form_link
):

    success = 0
    failed = 0

    for email in email_list:

        result = send_form_email(
            email.strip(),
            form_name,
            form_link
        )

        if result:
            success += 1
        else:
            failed += 1

    return {
        "success": success,
        "failed": failed
    }
