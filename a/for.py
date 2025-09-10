# mobile_forensics_tool_gui.py

import os
import subprocess
import hashlib
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from fpdf import FPDF
from PIL import Image, ImageTk
import threading
import sys

# Set the full path to your adb executable
ADB_PATH = r"C:\\platform-tools\\adb.exe"  # Update this path as needed
OUTPUT_DIR = "forensics_output"
LOG_FILE = os.path.join(OUTPUT_DIR, 'log.txt')
DEVICE_ID = ""

def log_message(msg):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(msg + "\n")

def get_device_id():
    try:
        output = subprocess.check_output([ADB_PATH, 'devices']).decode().splitlines()
        for line in output:
            if "\tdevice" in line:
                return line.split("\t")[0]
    except Exception as e:
        log_message(f"Error getting device ID: {str(e)}")
    return ""

def run_adb_command(cmd):
    full_cmd = [ADB_PATH]
    if DEVICE_ID:
        full_cmd += ['-s', DEVICE_ID]
    full_cmd += cmd
    try:
        result = subprocess.check_output(full_cmd, stderr=subprocess.STDOUT).decode()
        return result.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

def extract_basic_info():
    info = {
        'Manufacturer': run_adb_command(['shell', 'getprop', 'ro.product.manufacturer']),
        'Model': run_adb_command(['shell', 'getprop', 'ro.product.model']),
        'Android Version': run_adb_command(['shell', 'getprop', 'ro.build.version.release']),
        'Security Patch': run_adb_command(['shell', 'getprop', 'ro.build.version.security_patch']),
        'Boot Time': run_adb_command(['shell', 'uptime'])
    }
    return info

def pull_common_artifacts(log_func):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    paths = [
        ('/data/data/com.android.providers.telephony/databases/mmssms.db', 'sms.db'),
        ('/data/data/com.android.providers.contacts/databases/contacts2.db', 'contacts.db'),
        ('/data/data/com.android.providers.contacts/databases/calllog.db', 'calllog.db')
    ]
    for src, dest in paths:
        output_path = os.path.join(OUTPUT_DIR, dest)
        msg = f"[*] Pulling {src} to {output_path}"
        log_func(msg + "\n")
        log_message(msg)
        result = run_adb_command(['pull', src, output_path])
        log_func(result + "\n")
        log_message(result)

def generate_report(device_info):
    report_path = os.path.join(OUTPUT_DIR, 'report.txt')
    with open(report_path, 'w') as f:
        f.write(f"Mobile Forensics Report\nGenerated: {datetime.now()}\n\n")
        for key, value in device_info.items():
            f.write(f"{key}: {value}\n")
    return report_path

def generate_pdf_report(device_info):
    pdf_path = os.path.join(OUTPUT_DIR, 'report.pdf')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Mobile Forensics Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Generated: {datetime.now()}", ln=True)
    pdf.ln(10)
    for key, value in device_info.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)
    pdf.output(pdf_path)
    return pdf_path

def run_forensics(log_func):
    global DEVICE_ID
    DEVICE_ID = get_device_id()
    if not DEVICE_ID:
        log_func("[!] No Android device detected over USB.\n")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    log_func("\n=== Android Forensics Toolkit Started ===\n")
    log_message("=== Android Forensics Toolkit Started ===")
    info = extract_basic_info()
    for k, v in info.items():
        log_func(f"{k}: {v}\n")
        log_message(f"{k}: {v}")
    pull_common_artifacts(log_func)
    txt_path = generate_report(info)
    pdf_path = generate_pdf_report(info)
    log_func(f"\n[+] Text report saved to {txt_path}\n")
    log_func(f"[+] PDF report saved to {pdf_path}\n")
    log_message(f"[+] Text report saved to {txt_path}")
    log_message(f"[+] PDF report saved to {pdf_path}")

# GUI Setup
app = tk.Tk()
app.title("Android Forensics Toolkit")
app.geometry("700x500")

try:
    app.iconbitmap("icon.ico")
except:
    pass

def threaded_start():
    output_text.delete(1.0, tk.END)
    t = threading.Thread(target=run_forensics, args=(lambda msg: output_text.insert(tk.END, msg),))
    t.start()

def export_logs():
    if os.path.exists(LOG_FILE):
        messagebox.showinfo("Log File", f"Log file saved to: {LOG_FILE}")
    else:
        messagebox.showerror("Log File", "No log file found.")

start_button = tk.Button(app, text="Run Forensics", command=threaded_start, font=("Arial", 14), bg="blue", fg="white")
start_button.pack(pady=10)

export_button = tk.Button(app, text="Export Logs", command=export_logs, font=("Arial", 12))
export_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Courier", 10))
output_text.pack(expand=True, fill='both', padx=10, pady=10)

app.mainloop()
