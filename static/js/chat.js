/**
 * Created by vitkyk on 20.07.16.
 */
var ws;
var send_id;
var recv_id;
var online;

function init_recv(receiver_id) {
    recv_id = receiver_id;
}

function init_websocket(tornado_host, tornado_port, sender_id, username, token) {
    ws = new WebSocket("ws://" + tornado_host + ":" + tornado_port + "/ws/" + sender_id + "&" + username + '&' +token + "/");
    send_id = sender_id;
    ws.onmessage = function (evt) {
        var data = JSON.parse(evt.data);
        if (data['online']) {
            online = data['online'];
            $('#online').html(function() {
                var temp = '<ul>';
                for (var i = 0; i < online.length; i++){
                    temp += '<li><a href="/room/'+online[i]['id']+'">';
                    temp += online[i]['username'];
                    temp += '</a></li>';
                }
                temp += '</ul>';
                return temp;
            });
        } else {
            var name = data['name'];
            var text = data['text'];
            $('.table > tbody:last').append(
                '<tr><td class="col-md-4"><b>' + data["sender"] +
                ' -></b></td><td class="col-md-4"><b>' + data["receiver"] +
                ':</b></td><td class="col-md-8">' + text +'</td></tr>'
            );
        }

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
    $massage.val('');
    ws.send(JSON.stringify(data));
    return false;
});

