/**
 * Created by vitkyk on 20.07.16.
 */
var ws;
var send_id;
var recv_id;
//$('#msg_form').submit(function() {
//    var data = {
//        name: "django",
//        msg: "Hello, tornado!"
//    };
//    ws.send(JSON.stringify(data))
//    });

function init_websocket(sender_id, receiver_id) {
    ws = new WebSocket("ws://127.0.0.1:8888/ws/" + sender_id + "/");
    send_id = sender_id;
    recv_id = receiver_id;
    ws.onmessage = function (evt) {
        var data = JSON.parse(evt.data);
        var name = data['name'];
        var text = data['text'];
        console.log(evt);
        $('.table > tbody:last').append(
            '<tr><td class="col-md-4"><b>' + data["sender_id"] +
            ':</b></td><td class="col-md-4"><b>' + data["receiver_id"] +
            ':</b></td><td class="col-md-8">' + text +'</td></tr>'
        );
        var n = $(document).height();
        $('html, body').animate({ scrollTop: n });
    };

}

$('#msg_form').submit(function(){
    $massage = $("input[name='msg']");
    var data = {
        sender_id: send_id,
        receiver_id: recv_id,
        text: $massage.val()
    };
    //var msg = $massage.val();
    $massage.val('');
    ws.send(JSON.stringify(data));
    return false;
});

