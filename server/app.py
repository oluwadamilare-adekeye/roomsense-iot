import os
import re
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_bcrypt import Bcrypt

from database import engine, SessionLocal
from models import Base, SensorReading, User
from pubnub_client import get_pubnub

load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)

# -------------------------
# Security / session config
# -------------------------
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

IS_PROD = os.getenv("FLASK_ENV") == "production"
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=IS_PROD,  # True on AWS/HTTPS
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(days=3),
)

# Create tables (SQLite locally, Postgres later via DATABASE_URL)
Base.metadata.create_all(bind=engine)

# -------------------------
# Pages
# -------------------------

@app.get("/")
def home_page():
    if "user_id" in session:
        return redirect(url_for("dashboard_page"))
    return render_template("landing.html")


@app.get("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template(
        "dashboard.html",
        username=session.get("username"),
    )


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            return render_template("login.html", error="Please fill in all required fields!"), 400

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return render_template("login.html", error="Invalid email or password."), 401

            if not bcrypt.check_password_hash(user.password_hash, password):
                return render_template("login.html", error="Invalid email or password."), 401

            session.permanent = True
            session["user_id"] = user.id
            session["username"] = user.username

            return redirect(url_for("dashboard_page"))
        finally:
            db.close()

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        confirm_password = request.form.get("confirm_password") or ""

        # Required
        if not username or not email or not password:
            return render_template("register.html", error="Please fill in all required fields!"), 400

        if len(username) > 50:
            return render_template("register.html", long_username_error="Username must be 50 characters or fewer."), 400

        # Email format
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            return render_template("register.html", email_format_error="Invalid email format."), 400

        # Password strength: 8+, upper, lower, digit, special
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(password_regex, password):
            return render_template(
                "register.html",
                weak_password_error=(
                    "Password must be at least 8 characters long and include at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character."
                ),
            ), 400

        if confirm_password != password:
            return render_template("register.html", confirm_password_error="Passwords do not match."), 400

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                return render_template("register.html", existing_user_error="An account with this email already exists."), 400

            user = User(username=username, email=email, password_hash=password_hash)
            db.add(user)
            db.commit()

            return redirect(url_for("login_page"))
        except Exception:
            db.rollback()
            return render_template("register.html", error="An error occurred during registration. Please try again."), 500
        finally:
            db.close()

    return render_template("register.html")


@app.get("/logout")
def logout_page():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    db = SessionLocal()
    try:
        user = db.query(User).get(session["user_id"])
        if request.method == "POST":
            user.username = (request.form.get("username") or "").strip()
            user.email = (request.form.get("email") or "").strip().lower()
            db.commit()
            session["username"] = user.username
            return render_template("settings.html", username=user.username, email=user.email, success="Saved!")
        return render_template("settings.html", username=user.username, email=user.email)
    finally:
        db.close()

# -------------------------
# API
# -------------------------

@app.get("/api")
def api_index():
    return jsonify({
        "status": "RoomSense API running",
        "db_url_loaded": bool(os.getenv("DATABASE_URL")),
    })


@app.post("/api/test-insert")
def test_insert():
    session_db = SessionLocal()
    try:
        reading = SensorReading(motion=True, temperature=22.5, humidity=40.0)
        session_db.add(reading)
        session_db.commit()
        return jsonify({"ok": True, "inserted_id": reading.id})
    finally:
        session_db.close()


@app.get("/api/readings")
def list_readings():
    session_db = SessionLocal()
    try:
        readings = (
            session_db.query(SensorReading)
            .order_by(SensorReading.created_at.desc())
            .limit(50)
            .all()
        )
        return jsonify([
            {
                "id": r.id,
                "motion": r.motion,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in readings
        ])
    finally:
        session_db.close()


@app.post("/api/pubnub/publish-test")
def publish_test_to_pubnub():
    pubnub = get_pubnub()
    channel = os.getenv("PUBNUB_CHANNEL_EVENTS", "room.events")

    payload = {
        "device_id": "dev-simulator",
        "motion": True,
        "temperature": 23.1,
        "humidity": 42.0
    }

    pubnub.publish().channel(channel).message(payload).sync()
    return jsonify({"ok": True, "published_to": channel, "payload": payload})


if __name__ == "__main__":
    app.run(debug=True)