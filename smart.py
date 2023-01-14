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








# import argparse
# from utils.utility import helpText


# parser = argparse.ArgumentParser(description=helpText, formatter_class=argparse.RawTextHelpFormatter, add_help=False)
# parser.add_argument('-h', '--help', action='store_false', help='print this help message', default='False')
# parser.add_argument('-s', '--server', type=int, nargs='?', const=55452, help='Start the server')
# parser.add_argument('-c', '--client', type=str, help='Start the client')
# args = parser.parse_args()

# # print(vars(args))

# if args.server:
#     from functionality.server import start_server
#     items = args.server
#     start_server(items)


# elif args.client:
#     from functionality.client import start_client
#     items = args.client
#     if(":" in items):
#         items = items.split(":")
#         start_client(items[0], int(items[1]))
#     else:
#         start_client(items)

# else:
#     print("nope")
#     # print(helpText)