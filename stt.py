import speech_recognition as sr
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from kafka import KafkaProducer
# https://realpython.com/python-speech-recognition/
producer = KafkaProducer(bootstrap_servers='localhost:9094', client_id='prod_bonito',acks="all")

def record():

    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2,dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file 


def play():
    data, fs = sf.read("output.wav", dtype=np.int16)  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing

    
def transcribe():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=9)

    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(mic)
    #print("Capture ended.")

    # recognize (convert from speech to text)
    try:
        text = r.recognize_google(audio,language="pt-PT")
    except sr.UnknownValueError:
        #print("Could not understand audio uwu")
        return None
    print(text)
    return text

def debug():
    while True:
        try:
            print("""Select an option:
[1] Record
[2] Play
[3] Transcribe""")
            option = input("> ")
            if option == "1":
                record()
            elif option == "2":
                play()
            elif option == "3":
                transcribe()
            else:
                print("Invalid option")
        except KeyboardInterrupt:
            return


def request_song(song):
    producer.send('nerdj_play', song.encode('utf-8'))
    print(f"asking for {song}")

def parse_command(text):
    print(text)
    print(("música" in text))
    if ("música" in text):
        if "para" in text:
            producer.send('nerdj_simplecommand', b'stop')
            print("sent")
            return
        if "toca" in text:
            req = text.split("música")[1].strip()
            request_song(req)

def botloop():
    while True:
        text = transcribe()
        if text is not None:
            parse_command(text)
        


if __name__ == '__main__':

    botloop()