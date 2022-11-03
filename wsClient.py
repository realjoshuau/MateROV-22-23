import asyncio
import websockets
import msgpack

# Take messages from input(), msgpack them, and send them to the server
async def sendMsg(websocket, path):
    while True:
        data = input()
        data = msgpack.packb(data, use_bin_type=True)
        await websocket.send(data)

# Take messages from the server, msgpack them, and print them
async def recvMsg(websocket, path):
    async for message in websocket:
        data = msgpack.unpackb(message, raw=False)
        print(data)

async def main():
    # Connect to the server
    async with websockets.connect("ws://localhost:8765") as websocket:
        # Start the send and receive tasks
        sendTask = asyncio.create_task(sendMsg(websocket, "/"))
        recvTask = asyncio.create_task(recvMsg(websocket, "/"))
        # Wait for one of the tasks to finish
        done, pending = await asyncio.wait(
            [sendTask, recvTask],
            return_when=asyncio.FIRST_COMPLETED,
        )
        # Cancel the other task
        for task in pending:
            task.cancel()

asyncio.run(main())