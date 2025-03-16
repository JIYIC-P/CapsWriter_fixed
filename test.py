import os
import subprocess
import time
from typing import List
from pathlib import Path

# 启动 CapsWriter-Offline 客户端
def start_client():
    # 启动客户端进程
    client_process = subprocess.Popen(["python", "core_client.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return client_process

# 模拟用户输入
def simulate_input(client_process,files: List[Path]):
    # 模拟用户输入到客户端
    client_process.init_file(client_process,files)

# 获取识别结果
def get_recognition_result(client_process):
    # 从客户端的输出中获取识别结果
    result = client_process.stdout.readline().decode().strip()
    return result

# 人机对话程序
def chatbot():
    print("欢迎使用 CapsWriter-Offline 人机对话程序！")
    print("请按 CapsLock 键开始说话，松开后完成语音输入。")
    
    # 启动客户端
    client_process = start_client()
    
    while True:
        print("\n等待语音输入...")
        
        # 模拟用户输入（这里可以替换为实际的语音输入）
        simulate_input(client_process, "请说话")
        
        # 等待识别结果
        time.sleep(2)  # 等待 2 秒，等待识别完成
        recognition_result = get_recognition_result(client_process)
        
        if recognition_result:
            print(f"您说：{recognition_result}")
            
            # 根据识别结果进行响应
            if "你好" in recognition_result:
                print("CapsWriter：你好！很高兴和你聊天。")
            elif "再见" in recognition_result:
                print("CapsWriter：再见！期待下次和你聊天。")
                break
            else:
                print("CapsWriter：你说的是什么？我不太明白。")
        else:
            print("CapsWriter：没有检测到语音输入。")
    
    # 关闭客户端
    client_process.terminate()

# 主程序
if __name__ == "__main__":
    chatbot()