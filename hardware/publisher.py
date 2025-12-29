import os
from dotenv import load_dotenv
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

def get_pubnub():
    load_dotenv()
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
    pnconfig.user_id = os.getenv("PUBNUB_USER_ID", "roomsense-pi")
    return PubNub(pnconfig)

def publish_motion(motion: bool):
    pubnub = get_pubnub()
    channel = os.getenv("PUBNUB_CHANNEL_EVENTS", "room.events")

    payload = {
        "device_id": "pi400-01",
        "motion": motion
    }

    pubnub.publish().channel(channel).message(payload).sync()
    print(f"[HW] Published motion={motion}")