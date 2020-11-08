import argparse
import wave
import pyaudio

parser = argparse.ArgumentParser(description='Process convert binary file to .wav.')
parser.add_argument('-f', dest='file', type=str, help='binary file')
parser.add_argument('-rate', dest='RATE', type=int, default=44100, help='Audio rate')

args = parser.parse_args()

if __name__ == '__main__':
    frames = []
    with open(f"{args.file}", 'rb') as f:
        frames.append(f.read())
    waveFile = wave.open(f"{args.file}.wav", 'wb')
    waveFile.setnchannels(2)
    waveFile.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    waveFile.setframerate(args.RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
