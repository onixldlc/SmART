import socket
import sounddevice as sd
import numpy as np

class AudioRecorder:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.samplerate = 44100
        self.channels = 1
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))

    def audio_callback(self, indata, frames, time, status):
        audio = np.copy(indata)
        chunk_size = 256
        for i in range(0, audio.shape[0], chunk_size):
            chunk = audio[i:i+chunk_size]
            print(chunk.shape)
            self.client_socket.sendall(chunk.tostring())

    def start_recording(self):
        self.stream = sd.InputStream(callback=self.audio_callback, channels=self.channels, samplerate=self.samplerate)
        self.stream.start()

if __name__ == "__main__":
    ip = input("Enter the ip address of the server: ")
    print(ip)
    recorder = AudioRecorder(ip, 55452)
    recorder.start_recording()
    input("Press enter to stop recording.")
    recorder.stream.stop()
    recorder.client_socket.close()