from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64
import re
import requests


def gmail_service(token: str, refresh_token: str, client_id: str, client_secret: str):
    """Create Gmail API service using OAuth2 credentials."""
    creds = Credentials(
        token,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("gmail", "v1", credentials=creds)


def list_unsubscribe_messages(service):
    """Return messages that contain a List-Unsubscribe header."""
    resp = (
        service.users()
        .messages()
        .list(userId="me", q="has:list-unsubscribe", maxResults=100)
        .execute()
    )
    messages = []
    for m in resp.get("messages", []):
        msg = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=m["id"],
                format="metadata",
                metadataHeaders=["Subject", "From", "List-Unsubscribe"],
            )
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        messages.append(
            {
                "id": m["id"],
                "from": headers.get("From"),
                "subject": headers.get("Subject"),
                "unsubscribe": headers.get("List-Unsubscribe"),
            }
        )
    return messages


def unsubscribe_and_delete(service, message_id: str) -> int:
    """Unsubscribe using the List-Unsubscribe header and delete mail from sender.

    Returns the number of messages deleted.
    """
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "List-Unsubscribe"],
        )
        .execute()
    )
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    unsubscribe_hdr = headers.get("List-Unsubscribe")
    if not unsubscribe_hdr:
        return 0

    mailto_match = re.search(r"<mailto:([^>]+)>", unsubscribe_hdr)
    http_match = re.search(r"<(https?://[^>]+)>", unsubscribe_hdr)
    if mailto_match:
        unsub_addr = mailto_match.group(1)
        em = EmailMessage()
        em["To"] = unsub_addr
        em["Subject"] = "unsubscribe"
        service.users().messages().send(
            userId="me", body={"raw": base64.urlsafe_b64encode(em.as_bytes()).decode()}
        ).execute()
    if http_match:
        try:
            requests.get(http_match.group(1), timeout=10)
        except requests.RequestException:
            pass

    from_hdr = headers.get("From", "")
    match = re.search(r"<([^>]+)>", from_hdr)
    if not match:
        return 0
    from_addr = match.group(1)
    to_delete = (
        service.users()
        .messages()
        .list(userId="me", q=f"from:{from_addr}")
        .execute()
        .get("messages", [])
    )
    if to_delete:
        service.users().messages().batchDelete(
            userId="me", body={"ids": [m["id"] for m in to_delete]}
        ).execute()
    return len(to_delete)
