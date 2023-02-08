import tkinter as tk
import openai
import threading
import gtts
import os
import pygame
import random
import glob
import speech_recognition as sr

f = open("openai_api.txt")
openai.api_key = f.readline()


def generate_response(prompt):
   completions = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
   )

   message = completions.choices[0].text
   return message

def on_response(user_input, response):
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n")
    chat_history.insert(tk.END, f"ChatGPT: {response}\n")
    chat_history.config(state=tk.DISABLED)
    t = threading.Thread(target=run_audio_thread, args=(response,))
    t.start()

def run_audio_thread(response):
    random1 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p",
    "q","r","s","t","u","v","w","x","y","z"]
    rnd = random.sample(random1,int(len(random1)/2))
    test = "".join(rnd)
    tts = gtts.gTTS(response, lang='en-uk', slow=False)
    tts.save(test + ".mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(test + ".mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def stop():
    pygame.mixer.music.stop()
    

def get_response():
    try:
        files = glob.glob('*.mp3')
        for f in files:
            os.remove(f)
    except:
        pass
    user_input = entry.get()
    t = threading.Thread(target=run_response_thread, args=(user_input,))
    t.start()

def run_response_thread(user_input):
    response = generate_response(user_input)
    root.after(0, on_response, user_input, response)

def run_microphone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        user_input = r.recognize_google(audio)
        entry.delete(0, tk.END)
        entry.insert(0, user_input)
        get_response()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


root = tk.Tk()
root.title("ChatGPT GUI")
root.geometry("900x800")

frame = tk.Frame(root)
frame.pack()

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_history = tk.Text(frame, yscrollcommand=scrollbar.set, state=tk.DISABLED)
chat_history.pack(expand=True, fill=tk.BOTH)

lbl = tk.Label(root).pack()

scrollbar.config(command=chat_history.yview)

entry = tk.Entry(root, width=80)
entry.pack()

response_button = tk.Button(root, text="Get Response", command=get_response)
response_button.pack(padx=10,pady=10)

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.pack(padx=0,pady=0)

microphone_button = tk.Button(root, text="Speak", command=run_microphone)
microphone_button.pack(padx=15,pady=15)

root.mainloop()