import pandas as pd
import random
import numpy as np

data = []

for _ in range(500):

    skill_similarity = round(random.uniform(0.3, 1.0), 2)
    sessions_completed = random.randint(0, 15)
    rating = round(random.uniform(2.5, 5.0), 1)
    coding_submissions = random.randint(0, 30)
    discussion_activity = random.randint(0, 20)
    session_duration = random.randint(20, 120)
    response_time = random.randint(1, 15)

    # 🧠 More realistic success logic (weighted probability)
    score = (
        skill_similarity * 0.3 +
        (sessions_completed / 15) * 0.25 +
        (rating / 5) * 0.2 +
        (coding_submissions / 30) * 0.15 +
        (discussion_activity / 20) * 0.05 +
        (session_duration / 120) * 0.05
    )

    # Add noise
    score += np.random.normal(0, 0.05)

    learning_success = 1 if score > 0.55 else 0

    data.append([
        skill_similarity,
        sessions_completed,
        rating,
        coding_submissions,
        discussion_activity,
        session_duration,
        response_time,
        learning_success
    ])

columns = [
    "skill_similarity",
    "sessions_completed",
    "rating",
    "coding_submissions",
    "discussion_activity",
    "session_duration",
    "response_time",
    "learning_success"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv("learning_dataset.csv", index=False)

print("Realistic dataset generated 🚀")