import asyncio
import websockets
import json, msgpack
import base64
from pilot import Pilot
from message import JSONMessage

import logging
logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)
pilotSockets = []
coPilotSockets = []

# This websocket is super flaky. It's not clear why -- but if you get issues with it, restart it.
# This websocket is also not intended to be used in production. It's just a proof of concept.


async def processMsg(websocket, path):
    if websocket not in pilotSockets and websocket not in coPilotSockets:
        print("New socket: " + str(websocket))
        # # If socket doesn't ask to subscribe within 5 seconds, close it.
        # try:
        #     await asyncio.wait_for(websocket.recv(), timeout=5)
        # except asyncio.TimeoutError:
        #     print("Socket " + str(websocket) + " did not subscribe within 5 seconds; closing.")
        #     await websocket.close()
        #     return
    async for message in websocket:
        try:
            # See if message is bytes-like or string-like.
            msg = JSONMessage(message)
            if msg.command == "sub":
                if msg.role == "pilot":
                    pilotSockets.append(websocket)
                    print("New pilot socket: " + str(websocket))
                elif msg.role == "copilot":
                    coPilotSockets.append(websocket)
                    print("New co-pilot socket: " + str(websocket))
            elif msg.command == "unsub":
                if msg.role == "pilot":
                    pilotSockets.remove(websocket)
                    print("Removed pilot socket: " + str(websocket))
                elif msg.role == "copilot":
                    coPilotSockets.remove(websocket)
                    print("Removed co-pilot socket: " + str(websocket))
            elif msg.command == "msg":    
                if msg.role == "copilot":
                    for socket in pilotSockets:
                        await socket.send(message)
                        print("Sent message to pilot socket: " + str(socket))
                if msg.role == "pilot":
                    for socket in coPilotSockets:
                        await socket.send(message)
                        print("Sent message to co-pilot socket: " + str(socket))

        except Exception as e:
            print("Error: " + str(e))
            print("Websocket sent something we didn't understand: " + str(message))
            # Remove the socket from the list.
            if websocket in pilotSockets:
                pilotSockets.remove(websocket)
            if websocket in coPilotSockets:
                coPilotSockets.remove(websocket)
            
            # Close the socket.
            try:
                await websocket.close()
            except:
                pass
            finally:
                break # We no longer need to process messages from this socket. 

# Start a routine to print the number of sockets connected.
async def printNumSockets():
    while True:
        print("Pilot sockets: " + str(len(pilotSockets)))
        print("Co-pilot sockets: " + str(len(coPilotSockets)))
        await asyncio.sleep(5)


async def main():
    async with websockets.serve(processMsg, "localhost", 8765):
        await printNumSockets()
        await asyncio.Future()  # run forever

print("Server running on port 8765")
asyncio.run(main())