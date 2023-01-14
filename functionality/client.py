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
    recorder = AudioRecorder("192.168.0.123", 55452)
    recorder.start_recording()
    input("Press enter to stop recording.")
    recorder.stream.stop()
    recorder.client_socket.close()














# class AudioRecorder:
#     def __init__(self, ip, port, inTest=False):
#         self.ip = ip
#         self.port = port
#         self.samplerate = 44100
#         self.channels = 1
#         self.inTest = inTest
#         self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     def audio_callback(self, indata, frames, time, status):
#         audio = np.copy(indata)
#         self.client_socket.sendall(audio.tostring())

#     def start_recording(self):
#         self.client_socket.connect((self.ip, self.port))
#         try:
#             self.stream = sd.InputStream(callback=self.audio_callback, channels=self.channels, samplerate=self.samplerate)
#             self.stream.start()
#             while not self.inTest:
#                 pass
#         finally:
#             self.stop_recording()

#     def stop_recording(self):
#         self.stream.stop()
#         self.client_socket.close()


# if __name__ == "__main__":
#     player = AudioRecorder("127.0.0.1", 55452)
#     player.start_recording()



# def record_and_send_audio(ip, port):
#     if(ip == None):
#         print("IP Cannot be empty")
#         return

#     # Create a socket and connect to the server
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((ip, port))

#     # Set the audio format and settings
#     samplerate = 44100
#     channels = 1
#     inTest = False

#     # Open the default microphone and start recording audio
#     def audio_callback(indata, frames, time, status):
#         audio = np.copy(indata)
#         client_socket.sendall(audio.tostring())

#     stream = sd.InputStream(callback=audio_callback, channels=channels, samplerate=samplerate)
#     stream.start()

#     # Keep recording audio until the user stops the script
#     while True and not inTest:
#         pass

#     # Close the socket and stop recording audio
#     stream.stop()
#     client_socket.close()