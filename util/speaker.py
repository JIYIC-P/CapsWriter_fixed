import pyttsx3 as sp
def speak(text:str):
    s =sp.init()
    s.say(text)
    s.runAndWait()  
    s.stop()


if __name__ == "__main__":
    s = sp.init()

    while True:
        text = "戚文博是熊雅文儿子。"
        print(text)
        speak(text)
