
var wsHandler = {
    send: function(data){
        if (!this.state.connected){
            console.log("Not connected to server");
            this._queued.push(data);
            return;
        }
    },
    state: {
        "connected": false,
    },
    _queued: [],
    _ws: null,
    init: function(){
        if (window._ws.state.open){
            console.log("WebSocket already initialized -- handing off");
            this._ws = window._ws.ws;
            this.state.connected = true;
        }
        else{
            console.log("Initializing WebSocket");
            this._ws = new WebSocket("ws://localhost:8080/ws");
            this._ws.onopen = function(){
                console.log("WebSocket connected");
                this.state.connected = true;
                this._ws.onmessage = this.handleWSMsg;
                this._ws.onclose = function(){
                    console.log("WebSocket closed");
                    this.state.connected = false;
                    // TODO: Reconnect
                }
                for (var i = 0; i < this._queued.length; i++){
                    this._ws.send(this._queued[i]);
                }
                this._queued = [];
            }
        }
    },
    listeners: [], // {type: "missionTask", callback: function(data){}}
    _handleWSMsg: function(msg){
        // Handle messages from the server
        var packet = JSON.parse(msg.data);
        console.log("Received message from server: " + packet);
        if (packet.cmd != "update"){
            console.log("Received message from server that was not an update");
            return;
        }
    }
}