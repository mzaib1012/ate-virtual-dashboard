# Automated Test Equipment (ATE) Virtual Instruments Dashboard

A robust automated test framework built to demonstrate hardware-software orchestration, test automation pipelines, and telemetry analysis without physical hardware dependencies. The application acts as a central engineering console interfacing over virtual SCPI command buses to synchronize instruments, analyze waveforms, and log system compliance data.

## 🛠️ System Architecture & Features
- **Virtual Instrumentation Engine:** Implements software-defined emulators for an Arbitrary Waveform Generator (AWG) and a Digital Storage Oscilloscope (DSO).
- **SCPI Command Interrogation:** Fully utilizes Standard Commands for Programmable Instruments syntax mapping (e.g., `:FUNC`, `:FREQ`, `:MEAS:VPP?`) over a virtual abstraction layer.
- **Realistic Hardware Emulation:** Injects continuous white noise (Johnson–Nyquist emulation) and processes real mathematical signals to simulate physical component degradation and reading jitter.
- **Automated Validation Test Engine:** Run high-speed parameter sweeps across discrete frequency spectrums with real-time pass/fail evaluation based on dynamic guardbands.

## 📂 Project Tree Structure
```text
ate-virtual-dashboard/
│
├── README.md               # Engineering showcase documentation
├── requirements.txt        # External pipeline dependencies
│
├── app/
│   ├── main.py             # Main Streamlit Dashboard UI framework
│   └── instruments.py      # Core SCPI emulators for hardware components
│
└── logs/
    └── .gitkeep            # Deployment directory anchor
