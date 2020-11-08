import argparse
import socket
import pyaudio

FORMAT = pyaudio.paInt16

parser = argparse.ArgumentParser(description='Start UDP Server.')
parser.add_argument('-host', dest='HOST', type=str, default='127.0.0.1', help='Server host')
parser.add_argument('-port', dest='PORT', type=int, default=45777, help='Server Port')
parser.add_argument('-rate', dest='RATE', type=int, default=44100, help='Audio rate')
parser.add_argument('-chunk', dest='CHUNK', type=int, default=1024, help='Audio chunk size')
parser.add_argument('-channels', dest='CHANNELS', type=int, default=2, help='Audio channels count')

args = parser.parse_args()

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=args.CHANNELS,
                    rate=args.RATE,
                    input=True,
                    frames_per_buffer=args.CHUNK,
                    )

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect((args.HOST, args.PORT))
        with open('test_data', 'wb') as f:
            try:
                while True:
                    voice = stream.read(args.CHUNK)
                    s.sendall(voice)
                    f.write(voice)
            except KeyboardInterrupt:
                s.close()
