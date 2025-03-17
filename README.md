# CapsWriter_fixed
基于CapsWriter-Offline-master的语音识别器

## 1 流程图
### core_client.py
```mermaid
graph TD;
main[开始入口] --> A{判断启动参数};
A -->|是| init_file[init_file];
A -->|否| init_mic[init_mic];
```
