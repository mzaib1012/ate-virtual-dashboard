import streamlit as st
import pandas as pd
import numpy as np
import time
from instruments import VirtualSignalGenerator, VirtualOscilloscope

st.set_page_config(page_title="Automated Test Equipment Dashboard", layout="wide")

# Initialize persistent virtual instruments across app reruns
if "awg" not in st.session_state:
    st.session_state.awg = VirtualSignalGenerator()
if "dso" not in st.session_state:
    st.session_state.dso = VirtualOscilloscope(st.session_state.awg)

st.title("🔌 Automated Test Equipment (ATE) Dashboard")
st.markdown("---")

# Main Page Layout Split
col_control, col_plot = st.columns([1, 2])

with col_control:
    st.header("🎛️ Instrument Controls")
    
    # UI Control Inputs mapping directly to SCPI Emulation
    shape = st.selectbox("Waveform Shape (:FUNC)", ["SINE", "SQUARE", "TRIANGLE"])
    freq = st.slider("Target Frequency (Hz) (:FREQ)", 100, 5000, 1500, step=100)
    amp = st.slider("Target Amplitude (Vpp) (:VOLT)", 1.0, 10.0, 5.0, step=0.5)
    
    # Push changes to hardware core via virtual SCPI commands
    st.session_state.awg.write(f":FUNC {shape}")
    st.session_state.awg.write(f":FREQ {freq}")
    st.session_state.awg.write(f":VOLT {amp}")
    
    st.success("SCPI commands transmitted via virtual bus.")
    
    # Live Telemetry Display
    st.metric("Measured Vpp", f"{st.session_state.dso.query(':MEAS:VPP?')} V")
    st.metric("Measured Frequency", f"{st.session_state.dso.query(':MEAS:FREQ?')} Hz")

with col_plot:
    st.header("📊 Digital Storage Oscilloscope (DSO) Signal View")
    
    # Grab the current raw wave array from the oscilloscope
    t, signal = st.session_state.dso.capture_waveform()
    
    # Prepare data for Streamlit charting
    chart_data = pd.DataFrame({
        "Time (s)": t,
        "Amplitude (V)": signal
    }).set_index("Time (s)")
    
    st.line_chart(chart_data)

st.markdown("---")
st.header("🤖 ATE Automated Sequence Suite")
st.write("Click below to execute an automated compliance batch test across multiple frequency points.")

if st.button("🚀 Run Automated Compliance Sweep"):
    test_frequencies = [500, 1000, 2000, 3000, 4000]
    results = []
    
    progress_bar = st.progress(0)
    
    for i, f_test in enumerate(test_frequencies):
        # 1. Command hardware to the specific point
        st.session_state.awg.write(f":FREQ {f_test}")
        time.sleep(0.1) # Simulate hardware settling time
        
        # 2. Query values back via test bus
        v_read = float(st.session_state.dso.query(":MEAS:VPP?"))
        f_read = float(st.session_state.dso.query(":MEAS:FREQ?"))
        
        # 3. Simple Tolerance Pass/Fail Rule Engine (e.g., within 15% of target frequency)
        status = "PASS" if abs(f_read - f_test) / f_test < 0.15 else "FAIL"
        
        results.append({
            "Test Point": i + 1,
            "Target Freq (Hz)": f_test,
            "Measured Freq (Hz)": f_read,
            "Measured Vpp (V)": v_read,
            "Status": status
        })
        progress_bar.progress((i + 1) / len(test_frequencies))
        
    # Build results log DataFrame
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)
    
    # Export log feature
    csv_log = df_results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Save Pass/Fail Test Log Sheet (CSV)",
        data=csv_log,
        file_name="ATE_Compliance_Test_Log.csv",
        mime="text/csv"
    )
