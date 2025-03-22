import asyncio

async def send_message(message):
    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        asyncio.DatagramProtocol,
        remote_addr=('127.0.0.1', 9999)
    )
    print(f"发送消息: {message}")
    transport.sendto(message.encode())
    
if __name__ == "__main__" :
    try:
        while True:
            text = input("please make your choice:\n"
            "A:start\n"
            "B:stop\n"
            "C:cancle\n:")
            choice = ['start','stop','cancle']
            if text == "A":
                asyncio.run(send_message(choice[0]))
            elif text == "B":
                asyncio.run(send_message(choice[1]))
            elif text == "C":
                asyncio.run(send_message(choice[2]))

    except KeyboardInterrupt:
        print("exit")