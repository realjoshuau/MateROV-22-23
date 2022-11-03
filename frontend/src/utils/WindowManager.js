
import Webcam from "react-webcam";
import WinBox from 'react-winbox'
import React, { useState } from 'react';

function WindowManager(props){
    const {
        windows,
        setWindows
    } = props;
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

export default WindowManager;