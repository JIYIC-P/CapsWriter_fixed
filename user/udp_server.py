import asyncio
from user.usr_shortcut_handler import udp_mode
from util.client_cosmic import Cosmic
transport = None 
addr = ('127.0.0.1', 9999)
class EchoServerProtocol(asyncio.DatagramProtocol):
    
    def connection_made(self, transport):
        self.transport = transport
    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"收到来自 {addr} 的消息: {message}")
        udp_mode(message)

async def start():
    global transport
    transport, protocol = await Cosmic.loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 9999)
    )
    print("UDP服务器启动，监听端口9999...")

async def send(text:str):
    global transport 
    global addr
    await transport.sendto(text.encode(),addr=addr)

async def main():
    await start()
    while True:
        await asyncio.sleep(1000)

if __name__ == "__main__":
    Cosmic.loop = asyncio.get_event_loop()
    Cosmic.loop.run_until_complete(main())