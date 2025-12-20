import os
from pubnub.callbacks import SubscribeCallback
from pubnub.models.consumer.pubsub import PNMessageResult

from database import SessionLocal
from models import SensorReading


class RoomEventsListener(SubscribeCallback):
    def message(self, pubnub, message: PNMessageResult):
        data = message.message  # PubNub payload (dict)

        # Expected payload example:
        # {
        #   "device_id": "pi400-01",
        #   "motion": true,
        #   "temperature": 22.5,
        #   "humidity": 40.0
        # }

        motion = bool(data.get("motion", False))
        temperature = data.get("temperature", None)
        humidity = data.get("humidity", None)

        session = SessionLocal()
        try:
            reading = SensorReading(
                motion=motion,
                temperature=temperature,
                humidity=humidity
            )
            session.add(reading)
            session.commit()
            print(f"[PubNub] Inserted reading id={reading.id} from channel={message.channel}")
        except Exception as e:
            session.rollback()
            print(f"[PubNub] Failed to insert reading: {e}")
        finally:
            session.close()