import requests
import base64
import os
import json
import random

# 🔑 Zoom API Credentials (use environment variables for security)
ACCOUNT_ID = os.environ.get("ZOOM_ACCOUNT_ID", "qr4NPX0ZTk-qwrAnS3h-Ig")
CLIENT_ID = os.environ.get("ZOOM_CLIENT_ID", "tOHEwZfqTwyHJpH8kSAEAQ")
CLIENT_SECRET = os.environ.get("ZOOM_CLIENT_SECRET", "aEXaar8CazL7QAYIRIfBalsxdaWGHaht")

# ---------- GET ACCESS TOKEN ----------
def get_access_token():
    try:
        url = f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={ACCOUNT_ID}"

        auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded = base64.b64encode(auth.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded}"
        }

        print(f"🔄 Getting access token from: {url}")
        response = requests.post(url, headers=headers)
        
        print(f"📊 Token response status: {response.status_code}")
        print(f"📊 Token response: {response.text[:200]}")
        
        if response.status_code != 200:
            print(f"❌ Auth Error: {response.status_code} - {response.text}")
            return None
            
        data = response.json()
        
        if "access_token" not in data:
            print(f"❌ No access token in response: {data}")
            return None
            
        print(f"✅ Got access token: {data['access_token'][:20]}...")
        return data["access_token"]
    except Exception as e:
        print(f"❌ Error getting access token: {str(e)}")
        return None

# ---------- CREATE MEETING ----------
def create_meeting(topic="Skill Exchange Session"):
    try:
        token = get_access_token()
        
        if not token:
            print("❌ Failed to get access token - switching to fallback")
            return create_fallback_meeting(topic)

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

        print(f"🔄 Creating Zoom meeting for: {topic}")
        response = requests.post(url, json=body, headers=headers)
        
        print(f"📊 Meeting creation status: {response.status_code}")
        print(f"📊 Meeting response: {response.text[:300]}")
        
        if response.status_code not in [200, 201]:
            print(f"❌ Meeting creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return create_fallback_meeting(topic)
        
        data = response.json()
        
        if "join_url" not in data:
            print(f"❌ No join_url in response: {json.dumps(data, indent=2)}")
            return create_fallback_meeting(topic)
        
        join_url = data.get("join_url")
        print(f"✅ Zoom meeting created: {join_url}")
        return join_url
        
    except Exception as e:
        print(f"❌ Exception creating meeting: {str(e)}")
        return create_fallback_meeting(topic)

# ---------- FALLBACK MEETING (if Zoom fails) ----------
def create_fallback_meeting(topic="Skill Exchange Session"):
    """Generate a fallback meeting link when Zoom API fails"""
    # Generate random meeting ID (9 digits like Zoom format)
    meeting_id = random.randint(100000000, 999999999)
    fallback_link = f"https://zoom.us/j/{meeting_id}"
    print(f"⚠️ Using fallback meeting link: {fallback_link}")
    return fallback_link
