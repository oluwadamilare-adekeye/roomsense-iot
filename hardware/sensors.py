import RPi.GPIO as GPIO

PIR_PIN = 17
LED_PIN = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(PIR_PIN, GPIO.IN)          # PIR input
    GPIO.setup(LED_PIN, GPIO.OUT)         # LED output
    GPIO.output(LED_PIN, GPIO.LOW)

def read_motion() -> bool:
    return GPIO.input(PIR_PIN) == GPIO.HIGH

def set_led(motion: bool):
    GPIO.output(LED_PIN, GPIO.HIGH if motion else GPIO.LOW)

def cleanup():
    GPIO.output(LED_PIN, GPIO.LOW)