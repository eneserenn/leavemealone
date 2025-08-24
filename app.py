from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64
import re
import requests

app = FastAPI()


def gmail_service(token: str, refresh_token: str, client_id: str, client_secret: str):
    """Create a Gmail API service instance using OAuth2 credentials."""
    creds = Credentials(
        token,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("gmail", "v1", credentials=creds)


class Auth(BaseModel):
    token: str
    refresh_token: str
    client_id: str
    client_secret: str


@app.post("/subscriptions")
async def list_subscriptions(auth: Auth):
    """Return messages that contain an unsubscribe link."""
    service = gmail_service(**auth.dict())
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
    return {"messages": messages}


class UnsubRequest(Auth):
    message_id: str


@app.post("/unsubscribe")
async def unsubscribe(req: UnsubRequest):
    """Unsubscribe from a message and delete all mail from the sender."""
    service = gmail_service(
        token=req.token,
        refresh_token=req.refresh_token,
        client_id=req.client_id,
        client_secret=req.client_secret,
    )
    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=req.message_id,
            format="metadata",
            metadataHeaders=["From", "List-Unsubscribe"],
        )
        .execute()
    )
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    unsubscribe_hdr = headers.get("List-Unsubscribe")
    if not unsubscribe_hdr:
        raise HTTPException(status_code=400, detail="No unsubscribe header")

    mailto_match = re.search(r"<mailto:([^>]+)>", unsubscribe_hdr)
    http_match = re.search(r"<(https?://[^>]+)>", unsubscribe_hdr)
    if mailto_match:
        unsub_addr = mailto_match.group(1)
        em = EmailMessage()
        em["To"] = unsub_addr
        em["Subject"] = "unsubscribe"
        service.users().messages().send(
            userId="me",
            body={"raw": base64.urlsafe_b64encode(em.as_bytes()).decode()},
        ).execute()
    if http_match:
        requests.get(http_match.group(1), timeout=10)

    from_hdr = headers.get("From", "")
    match = re.search(r"<([^>]+)>", from_hdr)
    if match:
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
        deleted = len(to_delete)
    else:
        deleted = 0

    return {"status": "unsubscribed", "deleted": deleted}


