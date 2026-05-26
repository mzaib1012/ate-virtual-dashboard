import numpy as np
import time

class VirtualSignalGenerator:
    """Emulates an Arbitrary Waveform Generator (AWG) controlled via SCPI."""
    def __init__(self):
        self.shape = "SINE"
        self.frequency = 1000.0  # Hz
        self.amplitude = 5.0     # Vpp
        self.offset = 0.0        # V

    def write(self, command: str):
        """Processes SCPI write commands."""
        cmd = command.strip().upper()
        if cmd.startswith(":FUNC"):
            self.shape = cmd.split()[-1]
        elif cmd.startswith(":FREQ"):
            self.frequency = float(cmd.split()[-1])
        elif cmd.startswith(":VOLT"):
            self.amplitude = float(cmd.split()[-1])
        elif cmd.startswith(":OFFS"):
            self.offset = float(cmd.split()[-1])

    def query(self, command: str) -> str:
        """Processes SCPI query commands."""
        cmd = command.strip().upper()
        if cmd == ":FUNC?": return self.shape
        if cmd == ":FREQ?": return f"{self.frequency}"
        if cmd == ":VOLT?": return f"{self.amplitude}"
        if cmd == ":OFFS?": return f"{self.offset}"
        return "ERR: Unknown Command"


class VirtualOscilloscope:
    """Emulates a Digital Storage Oscilloscope (DSO) capturing noisy analog signals."""
    def __init__(self, generator: VirtualSignalGenerator):
        self.gen = generator
        self.sample_rate = 100000  # 100 kHz sample rate
        self.time_base = 0.005     # 5ms window size

    def capture_waveform(self):
        """Generates raw time-domain data based on current AWG physical states + noise."""
        t = np.linspace(0, self.time_base, int(self.sample_rate * self.time_base))
        
        # Base wave shape configurations
        if self.gen.shape == "SINE":
            wave = np.sin(2 * np.pi * self.gen.frequency * t)
        elif self.gen.shape == "SQUARE":
            wave = np.sign(np.sin(2 * np.pi * self.gen.frequency * t))
        elif self.gen.shape == "TRIANGLE":
            wave = 2 * np.abs(2 * (t * self.gen.frequency - np.floor(t * self.gen.frequency + 0.5))) - 1
        else:
            wave = np.zeros_like(t)

        # Apply gain (amplitude) and DC component shift
        signal = (self.gen.amplitude / 2) * wave + self.gen.offset
        
        # Add realistic Johnson-Nyquist hardware noise (0.05V variance)
        noise = np.random.normal(0, 0.15, size=t.shape)
        return t, signal + noise

    def query(self, command: str) -> str:
        """Processes measurement SCPI commands."""
        cmd = command.strip().upper()
        t, signal = self.capture_waveform()
        
        if cmd == ":MEAS:VPP?":
            vpp = np.max(signal) - np.min(signal)
            return f"{round(vpp, 3)}"
        elif cmd == ":MEAS:FREQ?":
            # Simple zero-crossing estimation to simulate hardware frequency counters
            zero_crossings = np.where(np.diff(np.sign(signal - np.mean(signal))))[0]
            if len(zero_crossings) > 1:
                period = (t[zero_crossings[-1]] - t[zero_crossings[0]]) / (len(zero_crossings)/2 - 1)
                freq = 1 / period
                return f"{round(freq, 1)}"
            return "0.0"
        return "ERR: Unknown Command"

print("✏️ Core virtual hardware instruments script successfully created at 'app/instruments.py'")
