from flask import Flask, jsonify, request
from gmail_service import (
    gmail_service,
    list_unsubscribe_messages,
    unsubscribe_and_delete,
)

app = Flask(__name__)


@app.post("/subscriptions")
def subscriptions():
    data = request.get_json(force=True)
    service = gmail_service(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
    )
    messages = list_unsubscribe_messages(service)
    return jsonify({"messages": messages})


@app.post("/unsubscribe")
def unsubscribe():
    data = request.get_json(force=True)
    message_id = data.get("message_id")
    service = gmail_service(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
    )
    deleted = unsubscribe_and_delete(service, message_id)
    return jsonify({"status": "unsubscribed", "deleted": deleted})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
