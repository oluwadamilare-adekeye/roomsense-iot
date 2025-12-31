import time
from sensors import read_motion, set_led, cleanup as sensors_cleanup
from buzzer import buzz_beep, buzz_off, cleanup as buzzer_cleanup
from publisher import publish_event

COOLDOWN_SECONDS = 5

def main():
    print("[HW] RoomSense hardware starting...")

    last_sent = 0

    try:
        while True:
            motion = read_motion()
            set_led(motion)

            now = time.time()

            if motion and (now - last_sent) >= COOLDOWN_SECONDS:
                print("[HW] Motion detected -> beep + publish")
                buzz_beep(0.2)

                publish_event({
                    "device_id": "pi-400",
                    "motion": True,
                    "ts": int(now)
                })

                last_sent = now

            if not motion:
                buzz_off()

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[HW] Stopping...")

    finally:
        sensors_cleanup()
        buzzer_cleanup()

if __name__ == "__main__":
    main()