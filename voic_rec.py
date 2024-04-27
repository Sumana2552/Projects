import tkinter as tk
from tkinter import messagebox
import wave
import pyaudio
import os
import threading
import time

class audio_recorder_app:
    def __init__(self, master):
        self.master = master
        master.title("Voice Recorder")

        self.duration_lbl = tk.Label(master, text="Duration (seconds):")
        self.duration_lbl.grid(row=0, column=0)

        self.entry_duration = tk.Entry(master)
        self.entry_duration.grid(row=0, column=1)

        self.record_button = tk.Button(master, text="Record", command=self.start_recording)
        self.record_button.grid(row=1, columnspan=2)

    def start_recording(self):
        try:
            duration = float(self.entry_duration.get())
            filename = "recorded_audio.wav"  

            self.rec_thread = threading.Thread(target=self.record, args=(filename, duration))
            self.rec_thread.start()

            self.record_button.config(state=tk.DISABLED)  
            self.master.after(int(duration * 1000), self.enable_rec_button)  
        except ValueError:
            messagebox.showerror("Error", "Invalid entry. Please enter a valid number.")

    def enable_rec_button(self):
        self.record_button.config(state=tk.NORMAL)

    def record(self, filename, duration, channels=2, s_rate=44100, size=1024, format=pyaudio.paInt16):
        frames = []

        p = pyaudio.PyAudio()

        stream = p.open(format=format,
                        channels=channels,
                        rate=s_rate,
                        input=True,
                        frames_per_buffer=size)

        print("Recording...")

        for i in range(0, int(s_rate / size * duration)):
            data = stream.read(size)
            frames.append(data)

        print("Your recording is complete!")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(s_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        messagebox.showinfo("Success", f"Audio recorded and saved as '{filename}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = audio_recorder_app(root)
    root.mainloop()
