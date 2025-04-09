import asyncio
from user import udp_server
from config import UDP 
from util.client_cosmic import Cosmic
import aioconsole
from user import excelprocess as ex
from user.reprocess import cut
import user.speaker as speaker

class CustomProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"收到来自 {addr} 的消息: {message}")
        # 调用自定义逻辑
        self.custom_handle(message)

    def custom_handle(self, message):
        name = cut(message)
        places = ex.where(name,ex.data)
        
        if len(places)==0:
            stences = speaker.sayings.回答_P_2 + name + speaker.sayings.回答_C_2
            
        else:
            stences = speaker.sayings.回答_P_1 + name 
            n = len(places)
            for i in range(n):
                stences += places[i]
            stences+=speaker.sayings.回答_C_1
        print(stences)
        speaker.speak(stences)
        


async def main():
    def protocol_factory():
        return CustomProtocol()  # 返回自定义协议实例
    server = udp_server.UDPserver()
    await server.start(local_addr=UDP.Clientaddr,protocol_factory=protocol_factory)  # 获取服务器对象
    try:
        while True:
            text = await aioconsole.ainput("please make your choice:\n"
            "A:start\n"
            "B:stop\n"
            "C:cancle\n:")
            choice = ['start','stop','cancle']
            if text == "A":
                server.send(choice[0],UDP.Serveraddr)
            elif text == "B":
                server.send(choice[1],UDP.Serveraddr)
            elif text == "C":
                server.send(choice[2],UDP.Serveraddr)
    except KeyboardInterrupt:
        print("exit")

if __name__ == "__main__" :
    path = "C:\\Users\\14676\\Desktop\\副本机房设备清单（正式版）.xlsx"
    ex.fix_excel(path)
    ex.data = ex.read(path)
    Cosmic.loop = asyncio.get_event_loop()
    Cosmic.loop.run_until_complete(main())