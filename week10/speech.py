"""Offline eSpeak NG synthesis; playback has an independent failure/stop result."""
import argparse
import ctypes
import ctypes.util
import os
from pathlib import Path
import shutil
import subprocess
import wave


def synthesize(text, destination):
    if not text.strip() or len(text) > 5000:
        raise ValueError('Speech needs 1 to 5000 characters.')
    name = os.environ.get('ESPEAK_LIBRARY') or ctypes.util.find_library('espeak-ng')
    if not name:
        raise RuntimeError('eSpeak NG library unavailable; answer remains visible and saved.')
    lib = ctypes.CDLL(name)
    lib.espeak_Initialize.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    data = os.environ.get('ESPEAK_DATA_PATH')
    rate = lib.espeak_Initialize(2, 0, data.encode() if data else None, 0)
    if rate <= 0:
        raise RuntimeError('eSpeak NG could not initialize its voice data.')
    chunks = []

    def receive(samples, count, events):
        if samples and count:
            chunks.append(ctypes.string_at(samples, count * 2))
        return 0

    callback = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_short),
                               ctypes.c_int, ctypes.c_void_p)(receive)
    try:
        lib.espeak_SetSynthCallback(callback)
        if lib.espeak_SetVoiceByName(b'en') != 0:
            raise RuntimeError('English voice unavailable.')
        lib.espeak_Synth.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.c_uint,
                                    ctypes.c_int, ctypes.c_uint, ctypes.c_uint,
                                    ctypes.c_void_p, ctypes.c_void_p]
        encoded = text.encode('utf-8')
        if lib.espeak_Synth(encoded, len(encoded) + 1, 0, 1, 0, 1, None, None) != 0:
            raise RuntimeError('Speech synthesis failed.')
        lib.espeak_Synchronize()
    finally:
        lib.espeak_Terminate()
    if not chunks:
        raise RuntimeError('Synthesis produced no audio.')
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destination), 'wb') as output:
        output.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
        output.writeframes(b''.join(chunks))
    return {'file': str(destination), 'rate': rate,
            'seconds': sum(map(len, chunks)) / 2 / rate, 'synthesized': True}


def play(path):
    executable = shutil.which('ffplay')
    if not executable:
        raise RuntimeError('ffplay unavailable. Open the WAV in an audio player; playback unverified.')
    process = subprocess.Popen([executable, '-nodisp', '-autoexit', '-loglevel', 'error', str(path)])
    try:
        if process.wait() != 0:
            raise RuntimeError('Playback failed; synthesized does not mean heard.')
    except KeyboardInterrupt:
        process.terminate()
        process.wait(timeout=5)
        return 'stopped'
    return 'player completed; listener must check audibility'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--text', default='Prepared speech check. This is not a handbook answer.')
    parser.add_argument('--out', default='out/speech-check.wav')
    parser.add_argument('--play', action='store_true')
    args = parser.parse_args()
    try:
        print(synthesize(args.text, args.out))
        if args.play:
            print('Ctrl+C stops playback.', flush=True)
            print(play(args.out))
    except (OSError, RuntimeError, ValueError) as error:
        parser.exit(1, f'Speech failed: {error}\n')


if __name__ == '__main__':
    main()
