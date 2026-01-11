import os
import time
import random
from dotenv import load_dotenv
from publisher import publish_event

load_dotenv()

DEVICE_ID = os.getenv("SIM_DEVICE_ID", "roomsense-sim-01")
INTERVAL = int(os.getenv("SIM_INTERVAL_SECONDS", "120"))

def generate_payload():
    return {
        "device_id": DEVICE_ID,
        "source": "sim",
        "temperature": round(random.uniform(18.0, 28.0), 1),
        "humidity": round(random.uniform(35.0, 70.0), 1),
        "motion": random.random() < 0.3,  # 30% chance
        "timestamp": int(time.time()),
    }

def main():
    print(f"[SIM] Device simulator started ({DEVICE_ID})")
    print(f"[SIM] Publishing every {INTERVAL} seconds")

    try:
        while True:
            payload = generate_payload()
            publish_event(payload)
            print("[SIM] Published:", payload)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n[SIM] Simulator stopped cleanly")

if __name__ == "__main__":
    main()