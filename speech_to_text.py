import json
import time

import pyaudio

import whisper
import wave

from audio_recorder import take_recording

CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 2  # Stereo audio
RATE = 44100  # Sampling rate (samples/second)

p = pyaudio.PyAudio()
default_output_device = 1


# for i in range(p.get_device_count()):
# device_info = p.get_device_info_by_index(i)
# print( p.get_device_info_by_index(i) )
# print(p.get_host_api_info_by_index(device_info["hostApi"])["name"])


def record():
    # Sampling frequency
    # Recording duration
    duration = 60 * 5
    print('*listening*')

    # Start recorder with the given values
    # of duration and sample frequency
    stream = p.open(format=FORMAT,
                    channels=2,
                    rate=RATE,
                    input=True,
                    input_device_index=default_output_device,
                    frames_per_buffer=CHUNK,
                    stream_callback=None)
    stream.start_stream()

    # Record audio and write to file
    output_file = wave.open("recorded.wav", "wb")
    output_file.setnchannels(CHANNELS)
    output_file.setsampwidth(p.get_sample_size(FORMAT))
    output_file.setframerate(RATE)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)
        output_file.writeframes(data)

    # Close the output file
    output_file.close()

    # clean
    stream.stop_stream()
    stream.close()
    p.terminate()


def transcribe(model, lang, path="./recorded.wav", *args, **kwargs):
    # result = model.transcribe("recorded.wav", prompt="Asystent" , fp16=False, task="translate", language='pl')
    result = model.transcribe(path, language=lang, task='translate', fp16=False)
    #print(json.dumps(result))
    return result['text']


# models = ["small.en", "tiny.en", 'base.en','medium.en','large.en', "small", "tiny", 'base','medium','large']
# for i in models:
#    try:
whisper_model = whisper.load_model('large', 'cpu')


# whisper_model = whisper.load_model('small')
#    except:
#        pass

def only_transcribe(lang, path="./recorded.wav"):
    return transcribe(whisper_model, lang, path=path)
def record_and_transcribe(lang):
    start = time.time()
    print("recording")
    take_recording()
    print(f"recording took {time.time() - start}")
    start = time.time()
    print("transcribe")
    message = transcribe(whisper_model, lang)
    print(f"transcribe took {time.time() - start}")
    print('USER: ', message)
    return message


if __name__ == '__main__':
    start = time.time()
    # message = transcribe(whisper_model)
    record_and_transcribe('pl')
