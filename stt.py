import speech_recognition as sr
import soundfile as sf
import sounddevice as sd
import numpy as np

from amqpstorm import UriConnection
from amqpstorm import Message
from scipy.io.wavfile import write

from nerde_door import opendoor

#conn = UriConnection('amqp://localhost:5672/%2f') # For Testing
conn = UriConnection('amqp://192.168.2.20:5672/%2f') # For Deployment

channel=conn.channel()
# https://realpython.com/python-speech-recognition/
channel.queue.declare('nerdj/cmd')
channel.queue.declare('nerdj/play')

#producer = KafkaProducer(bootstrap_servers='localhost:9094', client_id='prod_bonito',acks="all")

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
    mic = sr.Microphone()

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
    #producer.send('nerdj_play', song.encode('utf-8'))
    message = Message(channel, song)
    message.publish('nerdj/play')

    print(f"asking for {song}")

def nerdj_cmd(text:str):
    message = None
    if "para" in text or "parar" in text:
        message = Message(channel, 'stop')
    if "próxima" in text or "próximo" in text or "skip" in text:
        message = Message(channel, 'skip')
    if "pausa" in text or "pause" in text or "pausar" in text :
        message = Message(channel, 'pause')
    if message is not None:
        message.publish('nerdj/cmd')
    return



def parse_command(text):
    print(text)
    text=text.lower()
    print(("música" in text))
    if ("música" in text):
        if "toca" in text:
            req = text.split("música")[1].strip()
            req = text.split("já")[0].strip()
            request_song(req)
            return
        else:
            nerdj_cmd(text)
            return
    if ("abre" in text and "porta" in text) or ("abre-te sésamo" in text):
        opendoor()
    
        return
    
def botloop():
    while True:
        text = transcribe()
        if text is not None:
            parse_command(text)
        


if __name__ == '__main__':
    botloop()
