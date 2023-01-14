import socket
import numpy as np
import sounddevice as sd

class AudioPlayer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.samplerate = 44100
        self.channels = 1
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        self.client_socket = None

    def start_playing(self):
        print("Waiting for client to connect...")
        self.client_socket, address = self.server_socket.accept()
        print(f"Client {address} connected.")
        with sd.OutputStream(callback=self.audio_callback, blocksize=256):
            input("press Enter to stop the listening")
            self.client_socket.close()

#        try:
#            self.stream = sd.OutputStream(callback=self.audio_callback, channels=self.channels, samplerate=self.samplerate)
#            self.stream.start()
#            while True:
#                data = self.client_socket.recv(1024)
#                data2 = np.fromstring(data, dtype=np.float32)
#                data2 = data2.reshape(112,1)
#                data2 = data2.reshape(256,)
#                print("datashape: ", data2.shape)
#                if not data:
#                    break
#        finally:
#            self.stop_playing()
#            self.client_socket.close()

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

        #outdata[:] = data.reshape(-1, 1) if outdata.shape[1] == 1 else data.reshape(outdata.shape)


        #print("shape: ", data.shape)
        #if not data:
        #    outdata.fill(0)
        #    return sd.CallbackStop
        #outdata[:] = np.fromstring(data, dtype=np.float32)

if __name__ == "__main__":
    player = AudioPlayer("0.0.0.0", 55452)
    player.start_playing()























































# import socket
# import sounddevice as sd

# def start_server(PORT):
#     HOST = '0.0.0.0' 
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((HOST, PORT))
#     s.listen(5)

#     handle_connection(s)



# def check_connection(addr,conn):
#     if addr[0] != '127.0.0.1':
#         conn.close()
#         return True
#     return False



# def handle_connection(s:socket.socket):
#     conn, addr = s.accept()
#     # notRecognise = check_connection(addr,conn)

#     # if(notRecognise):
#     #     conn.close()
#     #     return

#     sample_rate = int(conn.recv(1024).decode())
#     num_channels = int(conn.recv(1024).decode())
#     sample_width = int(conn.recv(1024).decode())

#     while True:
#         data = conn.recv(1024)
#         if not data:
#             conn.close()
#             break
#         sd.play(data, sample_rate=sample_rate, num_channels=num_channels, sample_width=sample_width)
#     return False





    