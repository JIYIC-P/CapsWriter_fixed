import asyncio
from user.usr_shortcut_handler import udp_mode
from util.client_cosmic import Cosmic
from config import UDP

class UDPserver:
    def __init__(self):
        self.transport = None

    class EchoServerProtocol(asyncio.DatagramProtocol):
        """默认协议类"""
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            message = data.decode()
            print(f"收到来自 {addr} 的消息: {message}")
            udp_mode(message)  # 默认处理逻辑

    async def start(self, local_addr, protocol_factory=None,loop = None):
        """启动服务器，允许传入自定义协议工厂"""
        print("start:",loop)
        if protocol_factory is None:
            # 默认使用 EchoServerProtocol
            protocol_factory = lambda: self.EchoServerProtocol()
        if loop == None:
            self.transport, protocol = await Cosmic.loop.create_datagram_endpoint(
                protocol_factory,
                local_addr=local_addr
            )
        else :
            self.transport, protocol = await loop.create_datagram_endpoint(
                protocol_factory,
                local_addr=local_addr
            )
        print(f"UDP 服务器已启动，监听地址: {local_addr}")
        return self
    
    async def close(self):
        """关闭UDP服务器"""
        if not self._is_running:
            return

        print("正在关闭UDP服务器...")
        if self.transport:
            self.transport.close()
            await self._close_event.wait()  # 等待关闭完成
            self._is_running = False
            print("UDP服务器已关闭")

    def send(self, text: str, remote_addr):
        if self.transport:
            self.transport.sendto(text.encode(), remote_addr)
        else:
            print("UDP 服务器未启动，无法发送消息")
            
async def main():
    server = UDPserver()
    await server.start(local_addr=UDP.Serveraddr)  # 获取服务器对象
    while True:
        await asyncio.sleep(1000)  # 保持服务器运行

if __name__ == "__main__":
    Cosmic.loop = asyncio.get_event_loop()
    Cosmic.loop.run_until_complete(main())