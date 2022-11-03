import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

import reportWebVitals from './reportWebVitals';

import WindowManager from './utils/WindowManager';
import Webcam from 'react-webcam';
import msgpack from 'msgpack-lite';

const root = ReactDOM.createRoot(document.getElementById('root'));


function App(){
  const [pilotOrCopilot, setPilotOrCopilot] = useState(null);
  const [state, setState] = useState({
    webcams: [],
    missionTask: null,
    serialMonitor: null
  });

  const [windows, setWindows] = useState({})


  function setPoC(_){
    console.log("Setting pilot or copilot to " + _);
    // Register listeners:
    window._ws.state.listeners.push(function(e){
      console.log("Received message from server: ");
      console.log(e);
      e = msgpack.decode(e.data);
      console.log("Received decoded-message from server: " + e);
    });

    window._ws.state.listeners.push(handleWSMsg);

    if (_ === "pilot"){
      setPilotOrCopilot(_);
      // Send a message down the websocket to the server
      var msg = msgpack.encode({
        cmd: "sub",
        role: "pilot"
      });
      console.log("Sending message to server: " + msg)
      window._ws.ws.send(msg);
    } else {
      alert("copilot not implemented yet");
      setPilotOrCopilot(_);
      // Send a message down the websocket to the server
      var msg = msgpack.encode({
        cmd: "sub",
        role: "copilot"
      });
      console.log("Sending message to server: " + msg)
      window._ws.ws.send(msg)
    }
  }

  function handleWSMsg(msg){
    // Handle messages from the server
    msg = msgpack.decode(msg.data);
    console.log("Received message from server: " + msg);

    if (msg.cmd != "msg"){
      console.log("Received message from server that was not a message");
      return;
    }
      /*
      {
        "cmd": "msg",
        "role": "pilot", // You only receive messages from your role (pilot/copilot)
        "msg": {
          "type": "missionTask", // Can be "missionTask", "serialMonitor", "webcam"
          "data": {
            // Data depends on the type
          }
        }
      }
      */
    if (msg.msg.type === "missionTask"){
      setState({
        ...state,
        missionTask: msg.msg.data
      });
      console.log("New mission task: " + msg.msg.data);
    }
    if (msg.msg.type === "serialMonitor"){
      setState({
        ...state,
        serialMonitor: msg.msg.data
      });
      console.log("New serial monitor data: " + msg.msg.data);
    }
    if (msg.msg.type === "webcam"){
      // No.
      console.log("Received webcam message from server");
    }
  }

  window._debug = {
    setPoC: setPoC,
    sendToWS: function(msg){
      window._ws.ws.send(msgpack.encode(msg));
    }
  };
  if (pilotOrCopilot === null){
    return (
      <div>
        <h1>Are you the pilot or copilot?</h1>
        <button onClick={() => setPoC("pilot")}>Pilot</button>
        <button onClick={() => setPoC("copilot")}>Copilot</button>
      </div>
    )
  } else {
    return (
        <div>
          <WindowManager windows={[
            {
              id: "1",
              neededProps: {
                title: "Webcam",
                x: "center",
                y: "center",
                width: "400px",
                height: "400px",
              },
              child: <Webcam />,
            }
          ]}/>
      </div>
    )
  }
}

function rootRenderTimer(){
  root.render(<App />)
  console.log("Finished rendering at " + new Date().toLocaleTimeString() + ", approximately " + (Date.now() - window._ws.state.start) + "ms since start");
}
  rootRenderTimer();

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
