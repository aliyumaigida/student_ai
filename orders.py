import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import pyttsx3

# record 
def record_audio(filename="audio/input.wav", duration=5, fs=44100):

    print("\nRecording... Speak now")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

    sd.wait()

    write(filename, fs, recording)

    print("Recording saved")

    return filename


# model = whisper.load_model("tiny")
model = whisper.load_model("base")

# speech to text
def transcribe_audio(audio_file):

    result = model.transcribe(audio_file)

    text = result["text"]

    print("You said:", text)

    return text


# text to speech 
def speak(text):
    engine = pyttsx3.init()  # init new engine every time
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # ensure engine finishes cleanly