import os
import openai
from dotenv import load_dotenv
import json
import smtplib
import email
import imaplib
import mimetypes
import time
from email.header import decode_header
from email.message import EmailMessage
import re

load_dotenv('./.env')

def getSender():
    email_sender = os.getenv("EMAIL_ADDRESS")
    return email_sender

def getPwd():
    email_password = os.getenv("EMAIL_PASSWORD")
    return email_password

def draft_response(email):
    # Extract the relevant parts of the email. This assumes `email` is a python email.message.Message object.
    body_text = email.get_payload()

    # Set your OpenAI API key.
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Generate a response using the OpenAI API. 
    # Use the body text of the email as the user's message and ask the model to write a reply.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or whatever model you're using
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The email said: \n\n{body_text}\n\nWrite a reply:"},
        ],
        temperature=0.6,  # This controls the randomness of the output
        max_tokens=512,  # This is the maximum length of the output
    )

    # Extract the text of the response.
    response_text = response.choices[0].message['content'].strip()

    return response_text
    
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