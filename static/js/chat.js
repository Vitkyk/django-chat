/**
 * Created by vitkyk on 20.07.16.
 */
var ws = new WebSocket("ws://127.0.0.1:8888/ws");

$('#msg_form').submit(function() {
    var data = {
        name: "django",
        msg: "Hello, tornado!"
    };
    ws.send(JSON.stringify(data))
    });