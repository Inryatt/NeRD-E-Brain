import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 40)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.say("Eu sou uma puta badalhoca")
engine.runAndWait()