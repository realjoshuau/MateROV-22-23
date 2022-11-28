import asyncio, json, websockets

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

USERS: set = set()


async def register(websocket, path):
    USERS.add(websocket)
    # Send the current state to the new user
    await websocket.send(json.dumps(STATE))
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["cmd"] == "rawStateUpdate":
                STATE[data["key"]] = data["value"]
                # Send the new state to all users
                if USERS:
                    await websockets.broadcast(USERS, json.dumps({
                        "cmd": "update",
                        "state": STATE,
                    }))
            elif data["cmd"] == "get":
                await websocket.send(json.dumps(STATE[data["key"]]))
            elif data["cmd"] == "missionTask":
                if data["action"] == "add":
                    STATE["missionPlan"].append({
                        "name": data["name"],
                        "checked": False,
                    })
                elif data["action"] == "remove":
                    STATE["missionPlan"].pop(data["index"])
                elif data["action"] == "check":
                    STATE["missionPlan"][data["index"]]["checked"] = data["checked"]
                # Send the new state to all users
                if USERS:
                    await websockets.broadcast(USERS, json.dumps({
                        "cmd": "update",
                        "state": STATE,
                    }))
            elif data["cmd"] == "electrical": # Electrical shows a graph of data over time & current state
                if data["action"] == "add":
                    STATE["electrical"].append({
                        "name": data["name"],
                        "voltage": data["voltage"],
                        "current": data["current"],
                        "time": data["time"],
                    })
                elif data["action"] == "get":
                    await websocket.send(json.dumps(STATE["electrical"]))
                elif data["action"] == "listAllByTime":
                    # TODO: make sure time is sequential. probably just unixtime
                    await websocket.send(json.dumps(STATE["electrical"]))
            else:
                print("Unknown command: " + str(data["command"]))
    except Exception as e:
        print("Error: " + str(e))
    finally:
        USERS.remove(websocket)

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
