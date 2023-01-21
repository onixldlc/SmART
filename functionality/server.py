from utils.device_picker import deviceHandler
import argparse
import asyncio

class AudioPlayer:
    def __init__(self, ip, port, device):
        self.ip = ip
        self.port = port
        self.deviceHandler = deviceHandler()
        self.device_index = device
    
    def start_playing(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.server_handler())
        loop.run_until_complete(task)
        # loop.run_in_executor(None, loop.run_until_complete, task)
        # input("Press Enter to quit...\n")
        # task.cancel()
        # loop.stop()

    async def audio_callback(self, reader, writer):
        connect_from = writer.get_extra_info('peername')
        print(f"Client {connect_from[0]}:{connect_from[1]} connected.")
        while True:
            data = await reader.read(self.deviceHandler.CHUNK)
            if not data:
                break
            self.stream.write(data)
        print(f"Client {connect_from[0]}:{connect_from[1]} disconnected.")
        writer.close()

    async def server_handler(self):
        self.stream = self.deviceHandler.create_stream_handler(self.device_index)
        self.stream.start_stream()

        self.server = await asyncio.start_server(self.audio_callback, self.ip, self.port)
        print("Waiting for client to connect...")
        await self.server.serve_forever()





def create_parser():
    parser = argparse.ArgumentParser(description='Run in server mode')
    parser.add_argument("-p", "--port", help="specify port number", type=int, default=55452)
    parser.add_argument("-d", "--device", help="specify device index", type=int, default=-1)
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    device = args.device
    port = args.port

    player = AudioPlayer("0.0.0.0", port, device)
    player.start_playing()