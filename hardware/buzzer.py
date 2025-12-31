from gpiozero import Buzzer

BUZZER_PIN = 22
buzzer = Buzzer(BUZZER_PIN)

def buzz_on():
    buzzer.on()

def buzz_off():
    buzzer.off()

def buzz_beep(duration: float = 0.2):
    buzzer.beep(on_time=duration, off_time=duration, n=1, background=False)

def cleanup():
    buzzer.off()