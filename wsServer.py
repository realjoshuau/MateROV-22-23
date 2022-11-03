import asyncio
import websockets
import json, msgpack

import logging
logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)
pilotSockets = []
coPilotSockets = []

async def processMsg(websocket, path):
    async for message in websocket:
        data = msgpack.unpackb(message, raw=False)
        print("New message from " + str(websocket) + ": " + str(data))
        if data["cmd"] == "sub":
            if data["role"] == "pilot":
                pilotSockets.append(websocket)
                print("New pilot socket: " + str(websocket))
            elif data["role"] == "copilot":
                coPilotSockets.append(websocket)
                print("New co-pilot socket: " + str(websocket))
        elif data["cmd"] == "unsub":
            if data["role"] == "pilot":
                pilotSockets.remove(websocket)
                print("Removed pilot socket: " + str(websocket))
            elif data["role"] == "copilot":
                coPilotSockets.remove(websocket)
                print("Removed co-pilot socket: " + str(websocket))
        elif data["cmd"] == "msg":    
            for socket in pilotSockets:
                print("Sent message to pilot socket: " + str(socket))
                await socket.send(message)
            for socket in coPilotSockets:
                print("Sent message to co-pilot socket: " + str(socket))
                await socket.send(message)


async def main():
    async with websockets.serve(processMsg, "localhost", 8765):
        await asyncio.Future()  # run forever

print("Server running on port 8765")
asyncio.run(main())