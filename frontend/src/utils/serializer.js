import msgpack from 'msgpack-lite';



function decodeMsgpack(body){
    const reader = new FileReader();
    reader.readAsBinaryString(body);
    reader.onload = function(e){
        const data = e.target.result;
        var buffer = new Uint8Array(data.length);
        for (var i = 0; i < data.length; i++) {
            buffer[i] = data.charCodeAt(i);
        }
        const msg = msgpack.decode(buffer);
        return msg;
    }
}

function decodeMsgpack2(body){
    var blob = body;
    var arrayBuffer = null;
    arrayBuffer = new Response(blob).arrayBuffer();
    var data = msgpack.decode(new Uint8Array(arrayBuffer));
    return data;
}

function jsonBase64Encoder(data){
    //var b = btoa(JSON.stringify(data));
    //return b;
    return JSON.stringify(data);
}
function jsonBase64Decoder(data){
    //var b = atob(data);
    return JSON.parse(data);
}

function encoder(data){
    return jsonBase64Encoder(data);
}

function decoder(data){
    return jsonBase64Decoder(data);
}

export {
    decodeMsgpack,
    decodeMsgpack2,
    jsonBase64Encoder,
    jsonBase64Decoder,
    encoder,
    decoder
}
