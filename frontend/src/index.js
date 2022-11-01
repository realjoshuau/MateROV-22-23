import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import WinBox from 'react-winbox'

import reportWebVitals from './reportWebVitals';
import Webcam from "react-webcam";


function WindowManager(){
  const [windows, setWindows] = useState([
    {
      id: 1,
      neededProps: {
        title: 'Window 1',
      },
      child: <Webcam />
    },
    {
      id: 2,
      neededProps: {
        title: 'Window 2',
      },
      child: <Webcam />
    },
    {
      id: 3,
      neededProps: {
        title: 'Window 3',
      },
      child: <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" />
    },
    {
      id: 4,
      neededProps: {
        title: 'Window 4',
      },
      child: <iframe src="https://cdpn.io/vainsan/fullpage/QWKwPwv" />
    }
  ]);

  // This function is for manage `onclose` callback behavior and virtual DOM state.
  const handleClose = (force, id) => {
    let state = [...windows];
    const index = state.findIndex(info => info.id === id);
    if (index !== -1) {
      if (state[index].onclose && state[index].onclose(force))
        return true;                       // window-specific onclose, returns true if it does not need the default close process.
      state.splice(index, 1);
      setTimeout(() => setWindows(state)); // (Notice 5)to change winbox showing state in `onclose`, MUST wrap it within `setTimeout`
    }
  };

  return (
    <>
      {windows.map(info => (
        <WinBox 
          key={info.id} 
          id={info.id} 
          onclose={(force) => handleClose(force, info.id)}
          {...info.neededProps} // assign any props you want to WinBox
        >
          {info.child}
        </WinBox>
      ))}
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <div>
        <WindowManager />
    </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
