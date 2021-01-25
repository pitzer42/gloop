let socket = new WebSocket("wss://8080-cbeacebb-2e51-4659-a9d5-8d9fab791a55.ws-us03.gitpod.io/foo/join");

socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});

function send(msg){
    socket.send(msg)
}


////////////////////

let socket = new WebSocket("wss://8080-cbeacebb-2e51-4659-a9d5-8d9fab791a55.ws-us03.gitpod.io/bar/join");

socket.addEventListener('message', function (event) {
    console.log('Message from server ', event.data);
});

function send(msg){
    socket.send(msg)
}