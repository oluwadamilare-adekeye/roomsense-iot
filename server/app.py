import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from database import engine, SessionLocal
from models import Base, SensorReading

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return {
        "status": "RoomSense API running",
        "db_url_loaded": bool(os.getenv("DATABASE_URL")),
    }

@app.post("/api/test-insert")
def test_insert():
    """Inserts one dummy reading so you can prove DB storage without hardware."""
    session = SessionLocal()
    try:
        reading = SensorReading(motion=True, temperature=22.5, humidity=40.0)
        session.add(reading)
        session.commit()
        return jsonify({"ok": True, "inserted_id": reading.id})
    finally:
        session.close()

@app.get("/api/readings")
def list_readings():
    session = SessionLocal()
    try:
        readings = (
            session.query(SensorReading)
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
                "created_at": r.created_at.isoformat()
            }
            for r in readings
        ])
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)