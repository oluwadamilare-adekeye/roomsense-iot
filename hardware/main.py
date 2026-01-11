import time
import RPi.GPIO as GPIO

from sensors import setup as sensors_setup, read_motion, set_led, cleanup as sensors_cleanup
from buzzer import setup as buzzer_setup, buzz_beep, cleanup as buzzer_cleanup

# If you want PubNub publishing when motion happens:
# from publisher import publish_event

COOLDOWN_SECONDS = 2.0

def main():
    print("[HW] RoomSense hardware starting...")

    sensors_setup()
    buzzer_setup()

    last_trigger_time = 0.0

    try:
        while True:
            motion = read_motion()
            set_led(motion)

            now = time.time()
            if motion and (now - last_trigger_time) > COOLDOWN_SECONDS:
                print("[HW] Motion detected")
                buzz_beep(0.2)

                # publish_event({"device_id": "roomsense-pi", "motion": True})

                last_trigger_time = now

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[HW] Stopping...")

    finally:
        sensors_cleanup()
        buzzer_cleanup()
        GPIO.cleanup()

if __name__ == "__main__":
    main()