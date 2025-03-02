import tkinter as tk
from tkinter import ttk, scrolledtext
import sqlite3
import psutil
import threading
import time
import subprocess
import platform
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from loguru import logger

# Database setup
DB_FILE = "scan_results.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# GUI setup
root = tk.Tk()
root.title("Hypervisor Detection Tool")
root.geometry("900x650")
root.configure(bg="#121212")

# Label for status
status_label = tk.Label(root, text="Scan Status: Idle", font=("Arial", 18, "bold"), fg="#00FF00", bg="#121212")
status_label.pack(pady=10)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, mode="determinate")
progress_bar.pack(pady=10, fill=tk.X, padx=20)

# System Resource Frame
resource_frame = tk.LabelFrame(root, text="System Resources", font=("Verdana", 10, "bold"), fg="#FFFFFF", bg="#1E1E1E")
resource_frame.pack(pady=10, fill=tk.X, padx=20)

cpu_label = tk.Label(resource_frame, text="CPU Usage: --%", font=("Consolas", 12), fg="#FFCC00", bg="#1E1E1E")
cpu_label.pack()
ram_label = tk.Label(resource_frame, text="RAM Usage: --%", font=("Consolas", 12), fg="#FFCC00", bg="#1E1E1E")
ram_label.pack()

# Network Analysis Status
network_status_label = tk.Label(root, text="Network Status: Checking...", font=("Consolas", 12), fg="#FFCC00", bg="#121212")
network_status_label.pack(pady=10)

# Chart Frame
chart_frame = tk.Frame(root, bg="#121212")
chart_frame.pack(pady=10, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(5, 3), facecolor="#121212")
ax.set_facecolor("#121212")
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to check for hypervisor
def detect_hypervisor():
    progress_var.set(0)
    
    for i in range(1, 101, 20):
        time.sleep(0.2)
        progress_var.set(i)
        root.update_idletasks()

    is_vm = check_hypervisor()
    is_virtual_adapter = check_virtual_network_adapters()

    status = "Virtual Machine Detected!" if is_vm else "No VM Detected."
    network_status = "Virtual Network Adapter Found!" if is_virtual_adapter else "No Virtual Adapters."

    status_label.config(text=f"Scan Status: {status}", fg="#FF3333" if is_vm else "#00FF00")
    network_status_label.config(text=f"Network Status: {network_status}", fg="#FF3333" if is_virtual_adapter else "#00FF00")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scan_results (status) VALUES (?)", (status,))
    conn.commit()
    conn.close()
    
    update_chart()

# Update system resources
def update_system_resources():
    while True:
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        cpu_label.config(text=f"CPU Usage: {cpu_usage}%", fg="#FFCC00")
        ram_label.config(text=f"RAM Usage: {ram_usage}%", fg="#FFCC00")
        time.sleep(1)

# Update chart
def update_chart():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM scan_results")
    results = cursor.fetchall()
    conn.close()
    
    vm_count = sum(1 for r in results if "Virtual Machine" in r[0])
    no_vm_count = len(results) - vm_count

    ax.clear()
    ax.pie([vm_count, no_vm_count], labels=["VM Detected", "No VM"], colors=["#FF3333", "#00FF00"], autopct='%1.1f%%', startangle=90)
    ax.set_title("Detection Results", color="white")
    canvas.draw()

# Accurate Hypervisor Detection Function
def check_hypervisor():
    try:
        cpu_info = subprocess.check_output("wmic cpu get Caption,DeviceID,Manufacturer,MaxClockSpeed", shell=True).decode()
        if any(vm in cpu_info for vm in ["VMware", "VirtualBox", "KVM", "Hyper-V"]):
            return True
    except Exception as e:
        logger.error(f"Error in detection: {e}")

    return False

# Function to check for virtual network adapters
def check_virtual_network_adapters():
    try:
        adapters = psutil.net_if_addrs()
        for adapter in adapters.keys():
            if any(vm in adapter.lower() for vm in ["vmware", "virtual", "hyper-v", "vbox"]):
                return True
    except Exception as e:
        logger.error(f"Error checking network adapters: {e}")
    return False

# Function to fetch system specs
def get_system_specs():
    specs = []
    
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    specs.append(f"🖥️ CPU: {cpu_info}\n    Cores: {cpu_cores} | Threads: {cpu_threads}\n")

    ram = psutil.virtual_memory()
    specs.append(f"💾 RAM: {ram.total / (1024**3):.2f} GB Total\n    Available: {ram.available / (1024**3):.2f} GB\n")

    try:
        gpu_info = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], text=True).strip().split("\n")
        for idx, gpu in enumerate(gpu_info):
            name, vram = gpu.split(", ")
            specs.append(f"🎮 GPU {idx+1}: {name}\n    VRAM: {vram} MB\n")
    except:
        specs.append("🎮 GPU: No NVIDIA GPU detected.\n")

    for part in psutil.disk_partitions():
        if "cdrom" in part.opts or part.fstype == "":
            continue
        usage = psutil.disk_usage(part.mountpoint)
        specs.append(f"📀 Disk ({part.device}): {usage.total / (1024**3):.2f} GB\n    Free: {usage.free / (1024**3):.2f} GB\n")

    os_info = platform.system() + " " + platform.release()
    specs.append(f"🖥️ OS: {os_info}\n")

    return "\n".join(specs)

# Function to open the specs window
def open_system_specs():
    specs_window = tk.Toplevel(root)
    specs_window.title("System Specs")
    specs_window.geometry("700x500")
    specs_window.configure(bg="#0A0A0A")

    title_label = tk.Label(specs_window, text="🔧 SYSTEM INFORMATION 🔧", font=("Consolas", 16, "bold"), fg="#00FF00", bg="#0A0A0A")
    title_label.pack(pady=10)

    text_area = scrolledtext.ScrolledText(specs_window, wrap=tk.WORD, font=("Courier", 12), bg="#1A1A1A", fg="#00FF00", insertbackground="white")
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    text_area.insert(tk.END, get_system_specs())
    text_area.config(state=tk.DISABLED)

# Buttons
scan_button = tk.Button(root, text="Start Scan", font=("Consolas", 12, "bold"), fg="white", bg="#FF4500", command=lambda: threading.Thread(target=detect_hypervisor, daemon=True).start())
scan_button.pack(pady=10)
specs_button = tk.Button(root, text="View System Specs", font=("Consolas", 12, "bold"), fg="white", bg="#007BFF", command=open_system_specs)
specs_button.pack(pady=10)

threading.Thread(target=update_system_resources, daemon=True).start()

root.mainloop()
