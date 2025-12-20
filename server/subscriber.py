import os
from dotenv import load_dotenv

from pubnub_client import get_pubnub
from pubnub_listener import RoomEventsListener


def main():
    load_dotenv()

    pubnub = get_pubnub()
    events_channel = os.getenv("PUBNUB_CHANNEL_EVENTS", "room.events")

    pubnub.add_listener(RoomEventsListener())
    pubnub.subscribe().channels([events_channel]).execute()

    print(f"[Subscriber] Listening on PubNub channel: {events_channel}")
    print("[Subscriber] Press CTRL+C to stop.")

    # keep process alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Subscriber] Stopped.")


if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv

from pubnub_client import get_pubnub
from pubnub_listener import RoomEventsListener


def main():
    load_dotenv()

    pubnub = get_pubnub()
    events_channel = os.getenv("PUBNUB_CHANNEL_EVENTS", "room.events")

    pubnub.add_listener(RoomEventsListener())
    pubnub.subscribe().channels([events_channel]).execute()

    print(f"[Subscriber] Listening on PubNub channel: {events_channel}")
    print("[Subscriber] Press CTRL+C to stop.")

    # keep process alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[Subscriber] Stopped.")


if __name__ == "__main__":
    main()