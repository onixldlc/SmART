import sys

class WindowsInput:
    def __init__(self):
        import msvcrt
        self.input_method = msvcrt

    def config(self):
        pass
        
    def is_terminated(self):
        return self.input_method.kbhit() and ord(self.input_method.getch()) == 53
        
    def listen_key_press(self):
        pass

class LinuxInput:
    def __init__(self):
        import termios
        import tty
        self.input_method = {"termios":termios, "tty":tty}

    def config(self):
        self.input_method['fd'] = sys.stdin.fileno()
        self.input_method['original_termios'] = self.input_method['termios'].tcgetattr(self.input_method['fd'])
        self.input_method['tty'].setcbreak(self.input_method['fd'])
        
    def is_terminated(self):
        return sys.stdin.read(1) == "5"
        
    def listen_key_press(self):
        pass


def setup_input_method():
    platform = sys.platform
    if platform == "win32":
        return WindowsInput()
    elif platform == "linux" or platform == "linux2":
        return LinuxInput()