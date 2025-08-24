# leavemealone

Prototype FastAPI service that interacts with the Gmail API to list subscription
emails and help unsubscribe from them.

## Setup
1. Create a Google Cloud project and enable the Gmail API.
2. Obtain OAuth credentials and tokens for a Gmail account.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn app:app --reload
   ```

## Endpoints
- `POST /subscriptions` — list messages containing `List-Unsubscribe` headers.
- `POST /unsubscribe` — unsubscribe using the message id and remove existing mail
  from the sender.

Both endpoints expect OAuth tokens in the request body as shown in `app.py`.
