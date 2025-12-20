from pubnub.callbacks import SubscribeCallback
from pubnub.models.consumer.pubsub import PNMessageResult

from database import SessionLocal
from models import SensorReading


class RoomEventsListener(SubscribeCallback):
    def message(self, pubnub, message: PNMessageResult):
        data = message.message or {}  # PubNub payload (dict)

        motion = bool(data.get("motion", False))

        # cast safely
        try:
            temperature = float(data.get("temperature")) if data.get("temperature") is not None else None
        except (TypeError, ValueError):
            temperature = None

        try:
            humidity = float(data.get("humidity")) if data.get("humidity") is not None else None
        except (TypeError, ValueError):
            humidity = None

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