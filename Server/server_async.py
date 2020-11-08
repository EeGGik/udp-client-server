import argparse
import asyncio
import multiprocessing
import threading

parser = argparse.ArgumentParser(description='Start UDP Server.')
parser.add_argument('-host', dest='HOST', type=str, default='127.0.0.1', help='Server host')
parser.add_argument('-port', dest='PORT', type=int, default=45777, help='Server Port')
parser.add_argument('-w', dest='WORKERS', type=int, default=2, help='Servers workers')

args = parser.parse_args()


class AsyncWrite(threading.Thread):

    def __init__(self, text, out):
        # calling superclass init
        threading.Thread.__init__(self)
        self.text = text
        self.out = out

    def run(self):
        f = open(self.out, "ab")
        f.write(self.text)
        f.close()


class VoiceServer(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()
        print("Start consuming")

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        background = AsyncWrite(data, f'{addr[0]}:{addr[1]}')
        background.start()
        background.join()


def run_app():
    loop = asyncio.get_event_loop()
    t = loop.create_datagram_endpoint(VoiceServer, local_addr=(args.HOST, args.PORT), reuse_port=args.PORT)

    try:
        print(f'Server started on: {args.HOST} {args.PORT}')
        loop.run_until_complete(t)  # Server starts listening
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
        if loop.is_closed():
            print('Server is Stopped')
        else:
            print('Still alives')


if __name__ == '__main__':
    try:
        for i in range(args.WORKERS):
            process = multiprocessing.Process(target=run_app, args=())
            process.start()
            print(f"process {process} was started")
    except KeyboardInterrupt:
        for process in multiprocessing.active_children():
            process.terminate()
            process.join()
            print(f"process {process} was stopped")
