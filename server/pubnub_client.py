import os
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


def get_pubnub() -> PubNub: 
    publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
    subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    user_id = os.getenv("PUBNUB_USER_ID", "roomsense-server")

    if not publish_key or not subscribe_key:
        raise RuntimeError("Missing PUBNUB_PUBLISH_KEY or PUBNUB_SUBSCRIBE_KEY in environment variables.")

    pnconfig = PNConfiguration()
    pnconfig.publish_key = publish_key
    pnconfig.subscribe_key = subscribe_key
    pnconfig.user_id = user_id
    pnconfig.ssl = True  # TLS

    return PubNub(pnconfig)