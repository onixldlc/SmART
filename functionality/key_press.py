from functionality.input_method import setup_input_method

def send_stream(stream, s, CHUNK):
    data = stream.read(CHUNK)
    s.sendall(data)

def send_audio(stream, s, CHUNK, input_method):
    while True:
        send_stream(stream, s, CHUNK)
        if input_method.is_terminated():
            break
        input_method.listen_key_press()

def start_listening(stream, s):
    CHUNK = 1024
    input_method = setup_input_method()
    input_method.config()
    try:
        send_audio(stream, s, CHUNK, input_method)
    finally:
        if input_method.__class__.__name__ == "LinuxInput":
            input_method.termios.tcsetattr(input_method.fd, input_method.termios.TCSADRAIN, input_method.original_termios)