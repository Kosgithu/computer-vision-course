from machine import Pin
import time

# Configuration de la LED (Pin 2 est souvent la LED intégrée sur ESP32)
# Pour un Raspberry Pi Pico, utilisez Pin 25
led = Pin(2, Pin.OUT)

print("Début du clignotement MicroPython... (Ctrl+C pour arrêter)")

while True:
    led.value(1)  # Allumer
    time.sleep(0.5)
    led.value(0)  # Éteindre
    time.sleep(0.5)
