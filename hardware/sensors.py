import RPi.GPIO as GPIO

PIR_PIN = 17
LED_PIN = 27
BUZZER_PIN = 22

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def read_motion():
    return GPIO.input(PIR_PIN) == GPIO.HIGH

def set_outputs(motion: bool):
    GPIO.output(LED_PIN, GPIO.HIGH if motion else GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.HIGH if motion else GPIO.LOW)

def cleanup():
    GPIO.cleanup()
