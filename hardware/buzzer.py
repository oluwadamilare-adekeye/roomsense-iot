import time
import RPi.GPIO as GPIO

BUZZER_PIN = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def buzz_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzz_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def buzz_beep(duration: float = 0.2):
    buzz_on()
    time.sleep(duration)
    buzz_off()

def cleanup():
    GPIO.output(BUZZER_PIN, GPIO.LOW)