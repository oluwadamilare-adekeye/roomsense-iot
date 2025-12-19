import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()  # loads .env

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    return {
        "status": "RoomSense API running",
        "flask_env": os.getenv("FLASK_ENV"),
        "db_url_loaded": bool(os.getenv("DATABASE_URL")),
        "pubnub_keys_loaded": bool(os.getenv("PUBNUB_PUBLISH_KEY"))
    }

if __name__ == "__main__":
    app.run(debug=True)