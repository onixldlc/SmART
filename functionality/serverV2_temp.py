import socket
import numpy as np
import sounddevice as sd
from utils.device_picker import deviceHandler
import argparse
import pyaudio
import asyncio

class AudioPlayer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.deviceHandler = deviceHandler()
        
        self.device = self.deviceHandler.select_virtual_input()
        self.pyaudio = pyaudio.PyAudio()
        print(self.pyaudio.get_device_info_by_index(self.device))
        self.channels = 1
        self.samplerate = int(self.pyaudio.get_device_info_by_index(self.device)['defaultSampleRate'])
        self.CHUNK = 1024

        print(self.device, self.samplerate, self.channels)

        self.stream = self.pyaudio.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.samplerate,
            output=True,
            input_device_index=self.device,
            frames_per_buffer=self.CHUNK,
        )

    def start_playing(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.server_handler())
        loop.run_until_complete(asyncio.gather(task))
        input("Press Enter to quit...\n")
        task.cancel()
        loop.stop()

    async def audio_callback(self, reader, writer):
        # print(vars(self.stream))
        print(self.stream.is_active())
        while True:
            data = await reader.read(self.CHUNK)
            if not data:
                break
            self.stream.write(data)
        self.stream.stop_stream()
        writer.close()

    async def server_handler(self):
        self.stream.start_stream()
        server = await asyncio.start_server(self.audio_callback, self.ip, self.port)
        await server.serve_forever()





def create_parser():
    parser = argparse.ArgumentParser(description='Run in server mode')
    parser.add_argument("-p", "--port", help="specify port number", type=int, default=55452)
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    port = args.port

    player = AudioPlayer("0.0.0.0", port)
    player.start_playing()