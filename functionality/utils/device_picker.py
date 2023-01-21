import pyaudio

class deviceHandler():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device_count = self.p.get_device_count()
        self.device_index = self.p.get_default_input_device_info()['index']

        self.samplerate = int(self.p.get_device_info_by_index(self.device_index)['defaultSampleRate'])
        self.channels = 1
        self.CHUNK = 1024



    def create_stream_handler(self, device_index=-1):
        if(device_index > 0):
            self.device_index = device_index

            device = self.p.get_device_info_by_index(self.device_index)
            self.channels = device['maxOutputChannels']
            self.samplerate = int(device['defaultSampleRate'])
            print(device)
            print(self.device_index, self.samplerate, self.channels)
        else:
            self.select_virtual_input()

        print(self.device_index)

        return self.p.open(
            format=pyaudio.paFloat32,
            channels=self.channels,
            rate=self.samplerate,
            output=True,
            output_device_index=self.device_index,
            frames_per_buffer=self.CHUNK,
        )


    def select_virtual_input(self):
        self.printAllDevice()
        input_name = input("Enter the virtual input (empty=default, name=filter, number=device_index): ")
        if(input_name == ""):
            return self.device_index

        if(input_name.isnumeric()):
            self.device_index = int(input_name)
            return self.device_index
        
        self.device_count = self.filter_devices(self.device_count, input_name)
        if(len(self.device_count) > 1):
            for i, device in enumerate(self.device_count):
                print(i, device['name'], device['maxInputChannels'], "in", device['maxOutputChannels'], "out")
            selection = int(input("Select the device index:"))
            self.device_index = self.device_count[selection]['index']
        return self.device_index


    def printAllDevice(self):
        for i in range(self.device_count):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                print(i, device_info['name'], device_info['maxInputChannels'], "in", device_info['maxOutputChannels'], "out")


    def filter_devices(self, device_count, name):
        temp_devices = []
        for i in range(device_count):
            device_info = self.p.get_device_info_by_index(i)
            if device_info['name'].startswith(name):
                temp_devices.append(device_info)
        return temp_devices
