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
        try:
            # See if message is bytes-like or string-like.
            if isinstance(message, bytes):
                data = msgpack.unpackb(message, raw=False)
            else:
                print("Websocket did not send bytes-like object.")
                #data = json.loads(message)
                await websocket.send(json.dumps({
                    "error": "Please encode messages as msgpack."
                }));
                continue
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
        pass
        print("Pilot sockets: " + str(len(pilotSockets)))
        print("Co-pilot sockets: " + str(len(coPilotSockets)))
        await asyncio.sleep(5)

# Add the printNumSockets routine to the event loop.


async def main():
    async with websockets.serve(processMsg, "localhost", 8765):
        await printNumSockets()
        await asyncio.Future()  # run forever

print("Server running on port 8765")
asyncio.run(main())