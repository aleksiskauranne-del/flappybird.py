import numpy as np
import wave
import struct
import os

def save_wav(filename, samples, framerate=44100):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(s)))

def gen_sine(frequency, duration, amplitude=16000, framerate=44100):
    t = np.linspace(0, duration, int(framerate * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)

def gen_swoosh():
    # Rising then falling sine for 'swoosh'
    t = np.linspace(0, 0.3, int(44100 * 0.3), False)
    freq = np.linspace(400, 1200, len(t))
    samples = 12000 * np.sin(2 * np.pi * freq * t)
    return samples

def gen_wing():
    # Short, high blip
    return gen_sine(900, 0.08) * np.hanning(int(44100 * 0.08))

def gen_point():
    # Short, high-pitched beep
    return gen_sine(1400, 0.07) * np.hanning(int(44100 * 0.07))

def gen_hit():
    # Low, short thud
    return gen_sine(120, 0.12) * np.hanning(int(44100 * 0.12))

def gen_die():
    # Descending tone
    t = np.linspace(0, 0.5, int(44100 * 0.5), False)
    freq = np.linspace(900, 120, len(t))
    samples = 12000 * np.sin(2 * np.pi * freq * t)
    return samples

def main():
    os.makedirs('sounds', exist_ok=True)
    save_wav('swoosh.wav', gen_swoosh())
    save_wav('wing.wav', gen_wing())
    save_wav('point.wav', gen_point())
    save_wav('hit.wav', gen_hit())
    save_wav('die.wav', gen_die())
    print('All sound files generated!')

if __name__ == '__main__':
    main()
