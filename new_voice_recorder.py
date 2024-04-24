import streamlit as st 
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from pydub import AudioSegment
from noisereduce import reduce_noise
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def butter_worth_bandpass(lowcutfreq, highcutfreq, sampling_freq, order=5):
    nyq = 0.5 * sampling_freq #nyquist frequency 
    low = lowcutfreq / nyq
    high = highcutfreq / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_equalization(signal, lowcutfreq, highcutfreq, sampling_freq):
    b, a = butter_worth_bandpass(lowcutfreq, highcutfreq, sampling_freq)
    return filtfilt(b, a, signal)

def voice_record(filename, duration, s_rate):
    print("Recording....")
    myrecording = sd.rec(int(duration * s_rate), samplerate=s_rate, channels=2, dtype='int16')
    sd.wait()
    print("Recording Completed!!")
    wav.write(filename, s_rate, myrecording)



def main():
    st.title("Voc - The Voice Recording Application")
    st.sidebar.title("Settings")

    duration = st.sidebar.slider("Recording Duration(sec)", min_value=1, max_value = 120, value=5)
    sample_rate = st.sidebar.selectbox("Sample Rate", options=[44100, 48000, 96000], index=0)

    if st.sidebar.button("Record"):
        st.write("Recording in Progress...")
        filename = "rc.wav"
        voice_record(filename, duration, sample_rate)
        st.audio(filename, format='audio/wav')

        audio = AudioSegment.from_file(filename)

        audio_data = np.array(audio.get_array_of_samples())

        denoised_audio = reduce_noise(audio_data, sample_rate)

        #equalization
        lowcut_freq = 100 
        highcut_freq = 3000  
        equalized_audio = apply_equalization(denoised_audio, lowcut_freq, highcut_freq, sample_rate)

        # exporting the equalized audio
        equalized_filename = "rc1.wav"
        wav.write(equalized_filename, sample_rate, equalized_audio.astype(np.int16))
        
        st.success("Recording denoised, equalized, and saved as {}".format(equalized_filename))
    
if __name__ == "__main__":
    main()
