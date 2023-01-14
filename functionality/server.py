import socket
import numpy as np
import sounddevice as sd

class AudioPlayer:
    def __init__(self, ip, port, device):
        self.ip = ip
        self.port = port
        self.samplerate = 44100
        self.channels = 1
        self.device=device
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.client_socket = None

    def start_playing(self):
        print("Waiting for client to connect...")
        self.client_socket, address = self.server_socket.accept()
        print(f"Client {address} connected.")
        if(self.device==""):
            with sd.OutputStream(callback=self.audio_callback, blocksize=256):
                input("press Enter to stop the listening")
                self.client_socket.close()
        else:
            with sd.OutputStream(callback=self.audio_callback, blocksize=256, device=self.select_virtual_input(self.device)):
                input("press Enter to stop the listening")
                self.client_socket.close()

    def stop_playing(self):
        self.stream.stop()
        self.server_socket.close()

    def audio_callback(self, outdata, frames, time, status):
        data = self.client_socket.recv(1024)
        if not data:
            raise sd.CallbackStop
        data = np.frombuffer(data, dtype=np.float32)
        
        try:
            self.audio_buffer = np.concatenate((self.audio_buffer, data))
        except AttributeError:
            self.audio_buffer = data

        if len(self.audio_buffer) > frames:
            outdata[:] = self.audio_buffer[:frames].reshape(-1, 1)
            self.audio_buffer = self.audio_buffer[frames:]
        else:
            outdata[:] = np.zeros((frames,1))

    def select_virtual_input(self, name):
        devices = sd.query_devices()
        virtual_inputs = []
        for device in devices:
            if device['name'].startswith(name):
                virtual_inputs.append(device)
        if len(virtual_inputs)>1:
            for i, device in enumerate(virtual_inputs):
                print(i, device['name'])
            device_index = int(input("Select the device index:"))
            return device_index
        else:
            return virtual_inputs[0]['name']

if __name__ == "__main__":
    device = input("Enter the name of the output device you want to use (default output device):")
    player = AudioPlayer("0.0.0.0", 55452, device)
    player.start_playing()