import requests
import base64
import os

# 🔑 Zoom API Credentials (use environment variables for security)
ACCOUNT_ID = os.environ.get("ZOOM_ACCOUNT_ID", "qr4NPX0ZTk-qwrAnS3h-Ig")
CLIENT_ID = os.environ.get("ZOOM_CLIENT_ID", "tOHEwZfqTwyHJpH8kSAEAQ")
CLIENT_SECRET = os.environ.get("ZOOM_CLIENT_SECRET", "aEXaar8CazL7QAYIRIfBalsxdaWGHaht")

# ---------- GET ACCESS TOKEN ----------
def get_access_token():
    url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}"

    auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    return data["access_token"]

# ---------- CREATE MEETING ----------
def create_meeting(topic="Skill Exchange Session"):
    token = get_access_token()

    url = "https://api.zoom.us/v2/users/me/meetings"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "topic": topic,
        "type": 1,
        "settings": {
            "host_video": True,
            "participant_video": True
        }
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    return data.get("join_url")
