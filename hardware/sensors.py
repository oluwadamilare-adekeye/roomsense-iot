from gpiozero import MotionSensor, LED

# BCM pin numbers
PIR_PIN = 17
LED_PIN = 27

pir = MotionSensor(PIR_PIN)
led = LED(LED_PIN)

def read_motion() -> bool:
    return pir.motion_detected

def set_led(motion: bool):
    if motion:
        led.on()
    else:
        led.off()

def cleanup():
    # gpiozero handles cleanup, but we can turn things off safely
    led.off()