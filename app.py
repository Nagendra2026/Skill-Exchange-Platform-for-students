from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
import sqlite3
import os
import requests
from werkzeug.utils import secure_filename
from services.zoom import create_meeting
import joblib
import numpy as np
from ml_engine.matching import compute_similarity

app = Flask(__name__)
app.secret_key = "secret"

# ---------------- FILE UPLOAD CONFIG ----------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register-user", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    db = get_db()
    db.execute(
        "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
        (name, email, password, role)
    )
    db.commit()
    return redirect("/login")

# ---------------- LOGIN ----------------
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login-user", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    ).fetchone()

    if user:
        session["user"] = user["name"]
        session["id"] = user["id"]
        session["role"] = user["role"]

        if user["role"] == "faculty":
            return redirect("/faculty")
        else:
            return redirect("/dashboard")

    return "Invalid login"

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    if session.get("role") == "faculty":
        return redirect("/faculty")

    db = get_db()

    teach_skills = db.execute(
        "SELECT id,skill FROM skills WHERE user_id=? AND type='teach'",
        (session["id"],)
    ).fetchall()

    learn_skills = db.execute(
        "SELECT id,skill FROM skills WHERE user_id=? AND type='learn'",
        (session["id"],)
    ).fetchall()

    return render_template(
        "dashboard.html",
        name=session["user"],
        teach_skills=teach_skills,
        learn_skills=learn_skills
    )

# ---------------- ADD SKILL ----------------
@app.route("/add-skill-page")
def add_skill_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("add_skill.html")

@app.route("/add-skill", methods=["POST"])
def add_skill():
    data = request.get_json()
    skill = data["skill"]
    type = data["type"]

    db = get_db()
    db.execute(
        "INSERT INTO skills(user_id,skill,type) VALUES(?,?,?)",
        (session["id"], skill, type)
    )
    db.commit()

    return jsonify({"message": "Skill added successfully"})

# ---------------- DELETE SKILL ----------------
@app.route("/delete-skill/<int:id>")
def delete_skill(id):
    db = get_db()
    db.execute("DELETE FROM skills WHERE id=? AND user_id=?", (id, session["id"]))
    db.commit()
    return redirect("/dashboard")

# ---------------- EDIT SKILL ----------------
@app.route("/edit-skill/<int:id>")
def edit_skill_page(id):
    db = get_db()
    skill = db.execute("SELECT * FROM skills WHERE id=?", (id,)).fetchone()
    return render_template("edit_skill.html", skill=skill)

@app.route("/update-skill", methods=["POST"])
def update_skill():
    skill_id = request.form["id"]
    skill_name = request.form["skill"]
    skill_type = request.form["type"]

    db = get_db()
    db.execute(
        "UPDATE skills SET skill=?, type=? WHERE id=?",
        (skill_name, skill_type, skill_id)
    )
    db.commit()

    return redirect("/dashboard")

# ---------------- REQUEST SESSION ----------------
@app.route("/request-session", methods=["POST"])
def request_session():
    data = request.get_json()
    teacher_email = data["email"]
    skill = data["skill"]

    db = get_db()
    teacher = db.execute(
        "SELECT id FROM users WHERE email=?",
        (teacher_email,)
    ).fetchone()

    db.execute(
        "INSERT INTO sessions(teacher_id,learner_id,skill,status) VALUES(?,?,?,?)",
        (teacher["id"], session["id"], skill, "pending")
    )
    db.commit()

    return {"msg":"Session request sent"}

# ---------------- FACULTY PANEL ----------------
@app.route("/faculty")
def faculty_dashboard():
    if session.get("role") != "faculty":
        return redirect("/dashboard")

    db = get_db()

    sessions = db.execute("""
    SELECT sessions.id as sid,
           users.name as student,
           sessions.skill,
           sessions.status
    FROM sessions
    JOIN users ON sessions.learner_id = users.id
    ORDER BY sessions.id DESC
    """).fetchall()

    return render_template("faculty.html", sessions=sessions)

# ---------------- APPROVE SESSION ----------------
@app.route("/approve/<int:id>", methods=["POST"])
def approve(id):
    db = get_db()

    try:
        zoom_link = create_meeting()
    except:
        zoom_link = "https://zoom.us/j/123456789"

    db.execute(
        "UPDATE sessions SET status='approved', zoom_link=? WHERE id=?",
        (zoom_link, id)
    )
    db.commit()

    return "ok"
# ---------------- FIND MATCH ----------------
@app.route("/find-matches")
def find_matches():

    if "user" not in session:
        return redirect("/login")

    db = get_db()

    # get current student learn skills
    student_skills_data = db.execute(
        "SELECT skill FROM skills WHERE user_id=? AND type='learn'",
        (session["id"],)
    ).fetchall()

    student_skills = [row["skill"] for row in student_skills_data]

    # get all OTHER students who teach
    other_students = db.execute("""
        SELECT DISTINCT users.id, users.name, users.email
        FROM users
        JOIN skills ON users.id = skills.user_id
        WHERE users.id != ?
        AND skills.type='teach'
    """,(session["id"],)).fetchall()

    matches = []

    for student in other_students:

        teacher_skills_data = db.execute(
            "SELECT skill FROM skills WHERE user_id=? AND type='teach'",
            (student["id"],)
        ).fetchall()

        teacher_skills = [row["skill"] for row in teacher_skills_data]

        similarity = compute_similarity(student_skills, teacher_skills)

        if similarity > 0:
            matches.append({
                "teacher": student["name"],
                "email": student["email"],
                "similarity": round(similarity * 100, 2)
            })

    matches = sorted(matches, key=lambda x: x["similarity"], reverse=True)

    return render_template("matches.html", matches=matches)


# ---------------- REJECT SESSION ----------------
@app.route("/reject/<int:id>", methods=["POST"])
def reject(id):
    db = get_db()
    db.execute("UPDATE sessions SET status='rejected' WHERE id=?", (id,))
    db.commit()
    return "ok"

# ---------------- MY SESSIONS ----------------
@app.route("/my-sessions")
def my_sessions():
    db = get_db()

    sessions = db.execute("""
    SELECT users.name as teacher,
           sessions.skill,
           sessions.status,
           sessions.zoom_link
    FROM sessions
    JOIN users ON sessions.teacher_id = users.id
    WHERE sessions.learner_id=?
    ORDER BY sessions.id DESC
    """,(session["id"],)).fetchall()

    return render_template("my_sessions.html", sessions=sessions)




# ---------------- CODE EDITOR ----------------
@app.route("/code-editor")
def code_editor():
    if "user" not in session:
        return redirect("/login")
    return render_template("code_editor.html")

# ---------------- LEADERBOARD ----------------
@app.route("/leaderboard")
def leaderboard():
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    leaders = db.execute("""
    SELECT users.name, COUNT(submissions.id) as total
    FROM submissions
    JOIN users ON submissions.user_id = users.id
    GROUP BY submissions.user_id
    ORDER BY total DESC
    LIMIT 10
    """).fetchall()

    return render_template("leaderboard.html", leaders=leaders)

# ---------------- ANALYTICS ----------------
@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    total = db.execute(
        "SELECT COUNT(*) as count FROM submissions WHERE user_id=?",
        (session["id"],)
    ).fetchone()["count"]

    languages = db.execute("""
    SELECT language, COUNT(*) as total
    FROM submissions
    WHERE user_id=?
    GROUP BY language
    """,(session["id"],)).fetchall()

    recent = db.execute("""
    SELECT language, created_at
    FROM submissions
    WHERE user_id=?
    ORDER BY created_at DESC
    LIMIT 5
    """,(session["id"],)).fetchall()

    return render_template(
        "analytics.html",
        total=total,
        languages=languages,
        recent=recent
    )


# ---------------- CHAT DISCUSSIONS ----------------
@app.route("/discussions")
def discussions():
    db = get_db()
    topics = db.execute("SELECT * FROM discussions").fetchall()
    return render_template("discussions.html", topics=topics)

@app.route("/discussion/<int:id>")
def open_discussion(id):
    db = get_db()

    messages = db.execute("""
    SELECT users.name, discussion_messages.message, discussion_messages.file, discussion_messages.created_at
    FROM discussion_messages
    JOIN users ON discussion_messages.user_id = users.id
    WHERE discussion_id=?
    ORDER BY discussion_messages.created_at ASC
    """,(id,)).fetchall()

    return render_template("discussion_chat.html", messages=messages, did=id)

# ---------------- POST MESSAGE WITH FILE ----------------
@app.route("/post-message", methods=["POST"])
def post_message():

    discussion_id = request.form.get("discussion_id")
    message = request.form.get("message")
    file = request.files.get("file")

    filename = None

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    db = get_db()
    db.execute("""
    INSERT INTO discussion_messages(discussion_id,user_id,message,file)
    VALUES(?,?,?,?)
    """,(discussion_id, session["id"], message, filename))
    db.commit()

    return {"msg":"sent"}

# ---------------- SERVE UPLOADED FILES ----------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- GET MESSAGES FOR LIVE CHAT ----------------
@app.route("/get-messages/<int:discussion_id>")
def get_messages(discussion_id):

    db = get_db()

    messages = db.execute("""
    SELECT users.name,
           discussion_messages.message,
           discussion_messages.file,
           discussion_messages.created_at
    FROM discussion_messages
    JOIN users ON discussion_messages.user_id = users.id
    WHERE discussion_messages.discussion_id=?
    ORDER BY discussion_messages.id ASC
    """,(discussion_id,)).fetchall()

    return jsonify([dict(m) for m in messages])

# ---------------- SUBMIT CODE ----------------
@app.route("/submit-code", methods=["POST"])
def submit_code():
    if "user" not in session:
        return {"msg":"login required"}

    data = request.get_json()
    language = data["language"]
    code = data["code"]

    db = get_db()
    db.execute(
        "INSERT INTO submissions(user_id,language,code) VALUES(?,?,?)",
        (session["id"], language, code)
    )
    db.commit()

    return {"msg":"Code submitted"}
# ---------------- RUN CODE ----------------

import requests

@app.route("/run-code", methods=["POST"])
def run_code():
    try:
        data = request.get_json()
        code = data["code"]
        language = data.get("language", "python")

        # JDoodle language mapping
        languages = {
            "python": ("python3", "3"),
            "java": ("java", "4"),
            "c": ("c", "5"),
            "cpp": ("cpp17", "0"),
            "javascript": ("nodejs", "4")
        }

        lang, version = languages.get(language, ("python3", "3"))

        url = "https://api.jdoodle.com/v1/execute"

        payload = {
            "clientId": "7a3fd5e104cd621ed302b85c2a614e97",
            "clientSecret": "28e7a59d155fec047c90a1bb47caf23002398515fad0131166a789756e0e0123",
            "script": code,
            "language": lang,
            "versionIndex": version
        }

        response = requests.post(url, json=payload)
        result = response.json()

        output = result.get("output", "No Output")

        return {"output": output}

    except Exception as e:
        return {"output": f"Error: {str(e)}"}

# ---------------- AI HELP ----------------
@app.route("/ai-help", methods=["POST"])
def ai_help():
    data = request.get_json()
    code = data["code"]

    # simple AI logic (first version)
    suggestion = f"""
AI Analysis:

• Check syntax carefully
• Improve variable naming
• Add comments for clarity
• Optimize logic
• Handle edge cases

Code Review:
{code[:200]}

(Advanced AI integration can be added here)
"""

    return {"suggestion": suggestion}





# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- LOAD ML MODEL ----------------
model = joblib.load("ml_engine/learning_model.pkl")



# ---------------- PREDICT LEARNING SUCCESS ----------------
@app.route("/predict-success")
def predict_success():

    if "user" not in session:
        return redirect("/login")

    db = get_db()

    # Example feature extraction (you can improve later)
    sessions_completed = db.execute(
        "SELECT COUNT(*) as count FROM sessions WHERE learner_id=? AND status='approved'",
        (session["id"],)
    ).fetchone()["count"]

    coding_submissions = db.execute(
        "SELECT COUNT(*) as count FROM submissions WHERE user_id=?",
        (session["id"],)
    ).fetchone()["count"]

    discussion_activity = db.execute(
        "SELECT COUNT(*) as count FROM discussion_messages WHERE user_id=?",
        (session["id"],)
    ).fetchone()["count"]

    # Dummy placeholders (can improve later)
    skill_similarity = 0.75
    rating = 4.2
    session_duration = 60
    response_time = 5

    features = np.array([[ 
        skill_similarity,
        sessions_completed,
        rating,
        coding_submissions,
        discussion_activity,
        session_duration,
        response_time
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    return render_template(
        "prediction_result.html",
        prediction=prediction,
        probability=round(probability * 100, 2)
    )

# ----------------- FEATURE IMPORTANCE ----------------
import pandas as pd

@app.route("/feature-importance")
def feature_importance():

    if "user" not in session:
        return redirect("/login")

    df = pd.read_csv("ml_engine/feature_importance.csv")
    df = df.sort_values(by="importance", ascending=False)

    return render_template("feature_importance.html", data=df.to_dict(orient="records"))

# ----------------- CONFUSION MATRIX ----------------
@app.route("/confusion-matrix")
def show_confusion_matrix():
    if "user" not in session:
        return redirect("/login")
    return render_template("confusion_matrix.html")

# ----------------- ROC CURVE ----------------

@app.route("/roc-curve")
def show_roc():
    if "user" not in session:
        return redirect("/login")
    return render_template("roc_curve.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
