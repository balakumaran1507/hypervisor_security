# Hypervisor Detection Tool  

![License](https://img.shields.io/badge/license-MIT-blue.svg)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)  
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)  

## 📌 Overview  

The **Hypervisor Detection Tool** is a Python-based GUI application that detects whether the system is running inside a virtual machine (VM) or on physical hardware. The tool also provides system resource monitoring and logs results into an SQLite database.  

## ✨ Features  

✅ **Hypervisor Detection** – Identifies if the system is running inside a VM (e.g., VMware, VirtualBox, Hyper-V, KVM).  
✅ **Network Adapter Check** – Detects virtual network interfaces commonly associated with VM environments.  
✅ **System Resource Monitoring** – Displays real-time CPU and RAM usage.  
✅ **Graphical Representation** – Generates pie charts to visualize detection results.  
✅ **System Information Viewer** – Shows detailed system specifications including CPU, RAM, GPU, and disk info.  
✅ **Data Logging** – Stores scan results in an SQLite database for future reference.  

## 📸 Screenshots  

| Main Window | System Specs | Detection Graph |  
|------------|-------------|----------------|  
| ![Main Window](https://via.placeholder.com/300?text=Main+Window) | ![Specs](https://via.placeholder.com/300?text=System+Specs) | ![Graph](https://via.placeholder.com/300?text=Graph) |  

## 🛠️ Installation  

### **Requirements**  

- Python 3.8+  
- Tkinter (built-in with Python)  
- Required Python Libraries:  
  ```
  pip install psutil matplotlib loguru
  ```

### **Setup & Run**  

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/yourusername/hypervisor-detection.git
   cd hypervisor-detection
   ```

2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**  
   ```bash
   python main.py
   ```

## 🎯 How It Works  

1. Click the **"Start Scan"** button to begin the detection process.  
2. The tool checks for hypervisors and virtual network adapters.  
3. Detection results are displayed, logged, and plotted in a chart.  
4. Click **"View System Specs"** to see detailed system information.  

## 🔍 Detection Methods  

The tool detects VMs using:  

🔹 **CPU Information Analysis:** Scans CPU details for signs of virtualization (e.g., VMware, VirtualBox, Hyper-V).  
🔹 **Virtual Network Adapters:** Checks network interfaces for VM-related adapter names.  
🔹 **System Commands:** Uses `wmic` and `psutil` to gather system information.  

## 📂 Project Structure  

```
hypervisor-detection/
│── main.py               # Main application script
│── scan_results.db       # SQLite database for storing scan results
│── README.md             # Documentation
│── requirements.txt      # Required dependencies
```

## 🤝 Contributing  

Contributions are welcome! Feel free to fork this repository and submit a pull request.  

## 📜 License  

This project is licensed under the **MIT License** – you are free to use, modify, and distribute it.  

---

⭐ **If you find this tool useful, consider giving it a star on GitHub!** 🚀  
