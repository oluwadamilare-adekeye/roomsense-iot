import time
from sensors import setup_gpio, read_motion, set_outputs, cleanup
from publisher import publish_motion

def main():
    print("[HW] RoomSense hardware starting...")
    setup_gpio()

    try:
        while True:
            motion = read_motion()
            set_outputs(motion)

            if motion:
                publish_motion(True)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[HW] Stopping...")
    finally:
        cleanup()

if __name__ == "__main__":
    main()