# CapsWriter_fixed
基于CapsWriter-Offline-master的语音识别器

## 1.流程图
### core_client.py
```mermaid
graph TD;
main[开始入口] --> A{判断启动参数};
A -->|是| B[init_file带文件参数启动];
A -->|否| C[init_mic正常启动];
B --> D[others];
C -->|try| E["asyncio.run\(main_mic\(\)\),异步IO编程，可以使main_mic函数实现异步多线程运行"];
E --> F["调用client_cosmic.Cosmic类（公用类），初始化
    Cosmic.loop = asyncio.get_event_loop()
    Cosmic.queue_in = asyncio.Queue()
    Cosmic.queue_out = asyncio.Queue()"]
F --> G["show_mic_tips()调用cmd输出提示"]
G --> H["update_hot_all()跟新热词，通过文件读取pathlib.path()读取文件中热词,再通过hot_sub_zh.py中全局变量`热词词典`写入热词，为字典数据类型 key:词 values:拼音"]
H --> I["observe_hot()调用watchdog启动文件修改检测并添加处理函数（封装update_hot_all()）实现动态更新热词"]
```
    # 打开音频流
    Cosmic.stream = stream_open()

    # Ctrl-C 关闭音频流，触发自动重启
    signal.signal(signal.SIGINT, stream_close)

    # 绑定按键
    bond_shortcut()

    # 清空物理内存工作集
    if system() == 'Windows':
        empty_current_working_set()
