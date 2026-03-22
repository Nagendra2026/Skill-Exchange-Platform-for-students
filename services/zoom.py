import random
import re

# ---------------- JITSI MEETING ----------------
# We use Jitsi Meet for quick and robust video sessions without API auth.

def create_meeting(topic="Skill Exchange Session"):
    # Normalize topic text to safe room string
    safe_topic = re.sub(r"[^a-zA-Z0-9]", "", topic).lower()[:20]
    suffix = random.randint(1000, 9999)
    if not safe_topic:
        safe_topic = "skillexchange"
    room_name = f"{safe_topic}-{suffix}"
    join_url = f"https://meet.jit.si/{room_name}"
    print(f"✅ Jitsi meeting generated: {join_url}")
    return join_url

