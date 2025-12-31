import os
from dotenv import load_dotenv
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

load_dotenv()
def _get_pubnub() -> PubNub:
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
    pnconfig.user_id = os.getenv("PUBNUB_USER_ID", "roomsense-pi")
    if not pnconfig.subscribe_key or not pnconfig.publish_key:
        raise RuntimeError("Missing PUBNUB keys. Check your .env file on the Pi.")
    return PubNub(pnconfig)

_pubnub = _get_pubnub()

def publish_event(payload: dict):
    channel = os.getenv("PUBNUB_CHANNEL_EVENTS", "room.events")
    _pubnub.publish().channel(channel).message(payload).sync()