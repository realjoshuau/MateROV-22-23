import asyncio
import websockets
import json, msgpac
import base64

from message import JSONMessage
from database import Database

import logging
logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
)
STATE: dict = {
    "serialMonitor": [],
    "rovOrientation": {
        "roll": 0,
        "pitch": 0,
        "yaw": 0,
    },
    "clawSettings": {
        "claw1": {
            "state": "",
            "angle": 0,
        }
    },
    "electrical": [
        {
            "name": "Battery 1",
            "voltage": 0,
            "current": 0,
            "time": 0,
        },
    ],
    "missionPlan": [
        {
            "name": "Task 1",
            "checked": False,
        }
    ]
}

db = Database(checklist)

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
            elif msg.command == "completedTask":
                db.deleteTask()
            elif msg.command == "readTasks":
                for socket in coPilotSockets:
                    await socket.send(json.dumps(db.getTasks()))
                for socket in pilotSockets:
                    await socket.send(json.dumps(db.getTasks()))
                    
                        

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

# 

previousState = STATE
previousConnected: int = 0
async def debug_state():
    global previousState
    global previousConnected
    while True:
        if previousState != STATE:
            print(STATE)
            previousState = STATE
        if previousConnected != len(USERS):
            print(f"Connected: {len(USERS)}")
            previousConnected = len(USERS)
        await asyncio.sleep(0.1)

async def main():
    async with websockets.serve(register, "localhost", 8765):
        await printConnected()
        await asyncio.Future()  # run forever