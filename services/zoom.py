import requests
import base64

# 🔑 paste your keys here
ACCOUNT_ID = "PASTE_ACCOUNT_ID"
CLIENT_ID = "PASTE_CLIENT_ID"
CLIENT_SECRET = "PASTE_CLIENT_SECRET"

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
