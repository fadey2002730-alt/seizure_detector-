import streamlit as st
import mne
import numpy as np
import matplotlib.pyplot as plt
import os
st.set_page_config(page_title="محاكي كشف نوبات الصرع", layout="wide")
st.title("🧠 محاكي كشف نوبات الصرع بالذكاء الاصطناعي")
st.write("المشروع يستخدم داتا حقيقية من قاعدة CHB-MIT")
if st.button("ابدأ التحليل"):
    with st.spinner("جاري تحميل وتحليل الداتا..."):
        url = "https://physionet.org/files/chbmit/1.0.0/chb01/chb01_03.edf"
        edf_file = "chb01_03.edf"
        if not os.path.exists(edf_file):
            import urllib.request
            urllib.request.urlretrieve(url, edf_file)
        raw = mne.io.read_raw_edf(edf_file, preload=True, verbose=False)
        data = raw.get_data()
        sfreq = raw.info['sfreq']
        st.subheader("1. موجة EEG - قناة FP1")
        fig1, ax1 = plt.subplots(figsize=(12,3))
        ax1.plot(data[0, :2560])
        ax1.set_ylabel("uV")
        ax1.grid()
        st.pyplot(fig1)
        window_size = int(sfreq * 1)
        energies = []
        for i in range(0, data.shape[1] - window_size, window_size):
            window = data[0, i:i+window_size]
            energy = np.mean(window**2)
            energies.append(energy)
        threshold = np.mean(energies) + 3 * np.std(energies)
        seizure_detected = [i for i, e in enumerate(energies) if e > threshold]
        st.subheader("2. تحليل الطاقة وكشف النوبة")
        fig2, ax2 = plt.subplots(figsize=(12,3))
        ax2.plot(energies, label="طاقة الاشارة")
        ax2.axhline(y=threshold, color='r', linestyle='--', label="حد التنبيه")
        if len(seizure_detected) > 0:
            ax2.scatter(seizure_detected, [energies[i] for i in seizure_detected], color='red', label="نوبة مكتشفة")
        ax2.legend()
        ax2.grid()
        st.pyplot(fig2)
        st.subheader("3. النتيجة")
        if len(seizure_detected) > 0:
            st.error(f"⚠️ SEIZURE DETECTED! تم كشف نوبة في الثانية: {seizure_detected[0]}")
        else:
            st.success("✅ NORMAL - لا توجد نوبات")
st.write("---")
st.write("تم التطوير بواسطتك | داتا من PhysioNet CHB-MIT")
