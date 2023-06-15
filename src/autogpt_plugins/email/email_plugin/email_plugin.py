import os
import openai
import json
import smtplib
import email
import imaplib
import mimetypes
import time
from email.header import decode_header
from email.message import EmailMessage
import re

def getSender():
    email_sender = os.getenv("EMAIL_ADDRESS")
    return email_sender

def getPwd():
    email_password = os.getenv("EMAIL_PASSWORD")
    return email_password

def draft_response(email):
    # This is a placeholder function. You'll need to replace this with
    # your GPT model's inference function.
    return "This is a response to your email."

def save_draft(to: str, subject: str, body: str):
    email_sender = getSender()
    email_password = getPwd()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = email_sender
    msg["To"] = to
    msg.set_content(body)

    draft_folder = "[Gmail]/Drafts"

    conn = imap_open(draft_folder, email_sender, email_password)
    conn.append(
        draft_folder,
        "",
        imaplib.Time2Internaldate(time.time()),
        str(msg).encode("UTF-8"),
    )
    print(f"Draft saved to {draft_folder}!")

def read_emails(imap_folder: str = "inbox") -> None:
    email_sender = getSender()
    email_password = getPwd()

    conn = imap_open(imap_folder, email_sender, email_password)

    _, search_data = conn.search(None, "UNSEEN")

    email_ids = search_data[0].split()
    # If there are no unread emails, print a message and return
    if not email_ids:
        print("No unread emails found.")
        conn.logout()
        return

    # If there are unread emails, process them
    for num in email_ids:
        _, msg_data = conn.fetch(num, "(BODY.PEEK[])")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                from_address = msg["From"]
                to_address = msg["To"]
                response = draft_response(msg)
                save_draft(to_address, f"Re: {subject}", response)

    conn.logout()

def imap_open(
    imap_folder: str, email_sender: str, email_password: str
) -> imaplib.IMAP4_SSL:
    imap_server = os.getenv("EMAIL_IMAP_SERVER")
    conn = imaplib.IMAP4_SSL(imap_server)
    conn.login(email_sender, email_password)
    conn.select(imap_folder)
    return conn

def bothEmailAndPwdSet() -> bool:
    """Check if EMAIL_ADDRESS and EMAIL_PASSWORD are set in environment variables.
    Returns:
        bool: True if both EMAIL_ADDRESS and EMAIL_PASSWORD are set, False otherwise.
    """
    return 'EMAIL_ADDRESS' in os.environ and 'EMAIL_PASSWORD' in os.environ

# start the process
read_emails()