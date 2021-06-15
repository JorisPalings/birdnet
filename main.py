import pyaudio
import wave
import time
import threading
import subprocess

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 30


def analyse_recording(recording_filename):
    # Analyze the WAV file
    subprocess.run(["python3", "analyze.py",
                    "--i", recording_filename,
                    "--lat", "50.6397", "--lon", "4.6733",
                    "--min_conf", "0.25"])


while True:
    #  filename = 'recordings/' + time.strftime("%Y%m%d-%H%M%S") + ".wav"
    filename = 'recordings/' + str(int(time.time())) + ".wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('RECORDING AUDIO...', end=' ', flush=True)

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for n seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('DONE! Time', seconds, 'SECONDS')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    analysis_thread = threading.Thread(target=analyse_recording, args=(filename,))
    analysis_thread.start()
