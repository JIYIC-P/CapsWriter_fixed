import sys
from pathlib import Path
from multiprocessing import Queue
from typing import Dict, List
import websockets
from rich.console import Console 
console = Console(highlight=False)





class Cosmic:
    sockets: Dict[str, websockets.WebSocketClientProtocol] = {}
    sockets_id: List
    
    queue_in = Queue()
    #存放client传来的语音
    queue_out = Queue()
    #存放识别好的消息
