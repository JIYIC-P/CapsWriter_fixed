import pyttsx3 as sp
class sayings():
    回答_P_1 = "您好，您查找的"
    回答_P_2 = "您好，"
    回答_P_3 = "对不起，您查找的"
    回答_P_4 = "已经把"

    回答_C_1 = "在"
    回答_C_2 = "里是"
    回答_C_3 = "未检索到，请再试一次或退出"
    回答_C_4 = "放入"

    回答_w = "识别错误"

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
