from pynput.keyboard import Key, Controller
import time

keyboard = Controller()
print("Enter text for vwk: ", end = '')
text = str(input())
print("Enter vwk type speed (default 0.1s): ", end = '')
typeSpeed = float(input())

def presKey(key):
    keyboard.press(key)
    keyboard.release(key)

print("Prepare cursor on input field...")

time.sleep(5)

print("Starting vwk...")

for k in range(len(text)):
    if not text[k].isupper():
            presKey(text[k])
    if text[k].isupper():
        with keyboard.pressed(Key.shift):
            presKey(text[k])
    time.sleep(typeSpeed)