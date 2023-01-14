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