import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Run as a server or a client')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--server", help="run as server", action="store_true")
    group.add_argument("-c", "--client", help="run as client", action="store_true")
    parser.add_argument("-p", "--port", help="specify port number", type=int, default=55452)
    parser.add_argument("ip", nargs='?', help="specify ip address")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    print(vars(args))

    ip = args.ip
    port = args.port

    if args.server:
        print("Server mode")
    elif args.client:
        print("Client mode")
    else:
        parser.print_help()
    exit()

if __name__ == '__main__':
    main()
