import time
import pyperclip
from sender import send_clipboard

last_text = ""

while True:
    current = pyperclip.paste()
    if current != last_text:
        last_text = current
        print("Detected new clipboard, sending...")
        send_clipboard()
    time.sleep(0.2)
