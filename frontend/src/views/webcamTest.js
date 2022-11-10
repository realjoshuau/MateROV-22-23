import React from 'react';

var MyComponent = React.createClass({
  getInitialState: function(){
    return { videoSrc: null }
  },
  componentDidMount: function(){
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;
    if (navigator.getUserMedia) {
        navigator.getUserMedia({video: true}, this.handleVideo, this.videoError);
    }
  },
  handleVideo: function(stream) {
    // Update the state, triggering the component to re-render with the correct stream
    this.setState({ videoSrc: window.URL.createObjectURL(stream) });
  },
  videoError: function() {

  },
  render: function() {
    return <div>
      <video src={this.state.videoSrc} autoPlay="true" />
    </div>;
    }
});