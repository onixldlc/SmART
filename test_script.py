import socket
import unittest
import argparse
from unittest import mock
from unittest.mock import MagicMock, patch
import smart
from functionality.client import AudioRecorder
import random
import sounddevice as sd
import numpy as np
import wave

class TestArgumentParsing(unittest.TestCase):
    def test_server_default_port(self):
        parser = smart.create_parser()
        args = parser.parse_args(['-s'])
        self.assertTrue(args.server)
        self.assertEqual(str(args.port), str(55452))

    def test_server_custom_port(self):
        random_port = random.randint(10000, 65535) # random port number
        parser = smart.create_parser()
        args = parser.parse_args(['-s', '-p', str(random_port)])
        self.assertTrue(args.server)
        self.assertEqual(str(args.port), str(random_port))

    def test_client_default_port(self):
        parser = smart.create_parser()
        args = parser.parse_args(['-c', '127.0.0.1'])
        self.assertTrue(args.client)
        self.assertEqual(args.ip, '127.0.0.1')
        self.assertEqual(str(args.port), str(55452))

    def test_client_custom_port(self):
        random_port = random.randint(10000, 65535) # random port number
        parser = smart.create_parser()
        args = parser.parse_args(['-c', '127.0.0.1', '-p', str(random_port)])
        self.assertTrue(args.client)
        self.assertEqual(args.ip, '127.0.0.1')
        self.assertEqual(str(args.port), str(random_port))
    
    def test_client_empty(self):
        parser = smart.create_parser()
        # cm = self.assertLogs()
        args = parser.parse_args(['-c'])
        self.assertTrue(args.client)
        self.assertEqual(args.ip, None)
        # self.assertIn("IP Cannot be empty", cm.output)



class TestAudioRecorder(unittest.TestCase):
    def setUp(self):
        self.ip = '0.0.0.0'
        self.port = 55452
        self.recorder = AudioRecorder(self.ip, self.port, inTest=True)
        self.recorder.client_socket = MagicMock()
        self.addCleanup(self.recorder.client_socket.close)
        self.recorder.stream = MagicMock()

    @patch('numpy.copy')
    def test_audio_callback(self, copy_mock):
        indata = np.array([1, 2, 3])
        frames = 3
        time = 0.1
        status = None
        copy_mock.return_value = indata
        self.recorder.audio_callback(indata, frames, time, status)
        self.recorder.client_socket.sendall.assert_called_once_with(indata.tostring())

    @patch('sounddevice.InputStream')
    def test_start_recording(self, input_stream_mock):
        self.recorder.start_recording()
        self.recorder.client_socket.connect.assert_called_once_with((self.ip, self.port))
        input_stream_mock.assert_called_once_with(callback=self.recorder.audio_callback, channels=self.recorder.channels, samplerate=self.recorder.samplerate)
        self.recorder.stream.start.assert_called_once()
        self.recorder.stream.stop.assert_called_once()
        self.recorder.client_socket.close.assert_called_once()






















# class TestAudioRecorder(unittest.TestCase):
#     def setUp(self):
#         self.ip = '127.0.0.1'
#         self.port = 3000
#         self.recorder = AudioRecorder(self.ip, self.port)
#         self.audio_data = np.random.rand(44100, 1)

#     @patch('socket.socket')
#     @patch('sounddevice.InputStream')
#     def test_start_recording(self, mock_input_stream, mock_socket):
#         # Create mock socket and input stream objects
#         mock_client_socket = mock_socket.return_value
#         mock_input_stream.return_value = mock_input_stream
#         mock_client_socket.connect.return_value = None  # simulate a successful connection

#         # Configure the mock input stream to return the audio data
#         mock_input_stream.callback.side_effect = lambda *args: self.recorder.audio_callback(*args)
#         mock_input_stream.read.return_value = (self.audio_data, sd.CallbackFlags())

#         # Start the recording and wait for it to finish
#         self.recorder.start_recording()
#         self.recorder.inTest = True

#         # Assert that the audio data was sent to the server
#         mock_client_socket.sendall.assert_called_with(self.audio_data.tostring())































# class TestAudioRecorder(unittest.TestCase):
#     @patch('socket.socket')
#     @patch('sounddevice.InputStream')
#     def test_audio_recorder(self, mock_input_stream, mock_socket):
#         # Create mock objects
#         mock_client_socket = MagicMock()
#         mock_socket.return_value = mock_client_socket
#         mock_stream = MagicMock()
#         mock_input_stream.return_value = mock_stream

#         # Create AudioRecorder instance
#         recorder = AudioRecorder('127.0.0.1', 8000)

#         # Start recording
#         recorder.start_recording()

#         # Verify that the socket was created and connected
#         mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
#         mock_client_socket.connect.assert_called_once_with(('127.0.0.1', 8000))

#         # Verify that the input stream was created and started
#         mock_input_stream.assert_called_once_with(callback=recorder.audio_callback, channels=1, samplerate=44100)
#         mock_stream.start.assert_called_once()

#         # Simulate audio data being passed to the callback
#         indata = np.random.rand(1024, 1)
#         frames = 1024
#         time = 0
#         status = sd.CallbackFlags()
#         recorder.audio_callback(indata, frames, time, status)

#         # Verify that the audio data was sent to the server
#         mock_client_socket.sendall.assert_called_once()

#         # Stop recording
#         recorder.inTest = True
#         recorder.stop_recording()

#         # Verify that the stream was stopped and the socket was closed
#         mock_stream.stop.assert_called_once()
#         mock_client_socket.close.assert_called_once()













































# class TestAudioRecorder(unittest.TestCase):
#     def setUp(self):
#         self.ip = '127.0.0.1'
#         self.port = 55452
#         self.recorder = AudioRecorder(self.ip, self.port, True)

#         # Create a mock socket object
#         self.mock_socket = unittest.mock.Mock()
#         self.recorder.client_socket = self.mock_socket

#     # def test_audio_recording(self):
#     #     self.recorder.start_recording()
#     #     # Generate some test audio data
#     #     test_data = np.random.randint(-2**15, 2**15-1, 44100*5, np.int16)
#     #     # Send the test data to the "microphone"
#     #     sd.play(test_data, 44100)
#     #     # Wait for the test data to be sent to the server
#     #     sd.sleep(1)
#     #     self.recorder.inTest = True
#     #     # Check that the sendall method of the mock socket was called with the test data
#     #     self.mock_socket.sendall.assert_called_with(test_data.tostring())

#     def test_audio_music_with_wav(self):
#         self.recorder.start_recording()
#         waveHandler = wave.open("./Susu Murni Nasional W.O.Y Remix (Original)-I-cahWnSrPA.wav", "rb")
#         data = waveHandler.readframes(waveHandler.getnframes())
#         test_data = np.fromstring(data, dtype=np.int16)
#         rate = waveHandler.getframerate()*2
#         waveHandler.close()

#         strt_n_samples = rate * 12
#         ends_n_samples = rate * 15
#         test_data = test_data[strt_n_samples:ends_n_samples]

#         sd.play(test_data, rate)
#         self.mock_socket.sendall.assert_called_with(test_data)
















# class TestAudioRecorder(unittest.TestCase):
#     def setUp(self):
#         self.ip = '127.0.0.1'
#         self.port = 55452
#         self.recorder = AudioRecorder(self.ip, self.port)
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((self.ip, self.port))
#         self.server_socket.listen()
#         self.client_socket, self.client_address = self.server_socket.accept()

#     def tearDown(self):
#         self.client_socket.close()
#         self.server_socket.close()

#     def test_audio_recording(self):
#         self.recorder.start_recording()
#         # Generate some test audio data
#         test_data = np.random.randint(-2**15, 2**15-1, 44100*5, np.int16)
#         # Send the test data to the "microphone"
#         sd.play(test_data, 44100)
#         # Wait for the test data to be sent to the server
#         sd.sleep(5)
#         self.recorder.inTest = True
#         received_data = self.client_socket.recv(44100*5*2)
#         # Check that the received data is the same as the sent data
#         self.assertEqual(test_data.tostring(), received_data)





































    # def test_start_recording(self):
    #     recorder = AudioRecorder('127.0.0.1', 55452)
    #     recorder.client_socket = MagicMock()
    #     # recorder.inTest = True
    #     # recorder.start_recording()
    #     # recorder.client_socket.sendall.assert_called()


    #     recorder.inTest = True
    #     recorder.start_recording()
    #     recorder.client_socket.connect.assert_called_with(('127.0.0.1', 55452))
    #     recorder.client_socket.close.assert_called()

    #     sd.InputStream.stop.assert_called()

    # def test_start_recording(self):
    #     recorder = AudioRecorder('127.0.0.1', 55452)
    #     recorder.inTest = True
    #     recorder.start_recording()
    #     sd.InputStream.stop.assert_called()
    #     recorder.client_socket.close.assert_called()

    # def test_start_recording_custom_port(self):
    #     random_port = random.randint(10000, 65535) # random port number
    #     recorder = AudioRecorder('127.0.0.1', random_port)
    #     recorder.inTest = True
    #     recorder.start_recording()
    #     sd.InputStream.stop.assert_called()
    #     recorder.client_socket.close.assert_called()


    # def test_stop_recording(self):
    #     # Create a mock object for the audio input
    #     audio_data = b'audio_data'
    #     frames = 10
    #     time = 0.1
    #     status = sd.CallbackFlags()
    #     indata = (audio_data, frames, time, status)
        
    #     # Create a mock object for the socket
    #     client_socket = MagicMock()
    #     client_socket.sendall = MagicMock()
    #     client_socket.close = MagicMock()

    #     # Call the audio_callback function
    #     client.inTest = False
    #     client.audio_callback(indata, client_socket)
        
    #     # check that the loop is running
    #     self.assertFalse(client.inTest)
        
    #     # set inTest to true
    #     client.inTest = True
    #     client.audio_callback(indata, client_socket)
        
    #     # check that the loop is not running anymore
    #     self.assertTrue(client.inTest)
    #     # check that the socket was closed
    #     client_socket.close.assert_called()
    #     # check that the stream was stopped
    #     sd.InputStream.stop.assert_called()

    # def test_record_and_send_audio_with_empty_ip(self, mock_input_stream, mock_socket):
    #     # arrange
    #     ip = ""
    #     port = 55452
    #     cm = self.assertLogs()

    #     client.record_and_send_audio(ip, port)
    #     self.assertIn("IP Cannot be empty", cm.output)

        # capture the output
        #     # act
        #     client.record_and_send_audio(ip, port)
        
        
        # assert
        # self.assertEqual(cm.output, ["ERROR:root:IP Cannot be empty"])


    # @mock.patch('socket.socket')
    # @mock.patch('sounddevice.InputStream')
    # def test_record_and_send_audio(self, mock_input_stream, mock_socket):
    #     # arrange
    #     ip = '127.0.0.1'
    #     port = 55452

    #     # act
    #     client.record_and_send_audio(ip, port)

    #     # assert
    #     mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
    #     mock_socket.connect.assert_called_with((ip, port))
    #     mock_input_stream.assert_called_with(callback=mock_input_stream.callback, channels=1, samplerate=44100)
    #     mock_input_stream.start.assert_called()
    #     mock_input_stream.stop.assert_called()
    #     mock_socket.close.assert_called()




# class TestArgumentParsing(unittest.TestCase):
#     def test_server_mode(self):
#         # Test that the script runs in server mode when the -s argument is passed
#         parser = smart.create_parser()
#         args = parser.parse_args(['-s'])
#         self.assertTrue(args.server)
#         self.assertEqual(args.port, 55452)

#     def test_client_mode(self):
#         # Test that the script runs in client mode when the -c argument is passed
#         parser = smart.create_parser()
#         args = parser.parse_args(['-c', '127.0.0.1'])
#         self.assertTrue(args.client)
#         self.assertEqual(args.client[0], '127.0.0.1')
#         self.assertEqual(args.port, 55452)

#     def test_random_port(self):
#         # Test that the script uses a randomized port number when specified
#         random_port = random.randint(10000, 65535) # random port number
#         parser = smart.create_parser()
#         args = parser.parse_args(['-s', '-p', str(random_port)])
#         self.assertTrue(args.server)
#         self.assertEqual(args.port, str(random_port))