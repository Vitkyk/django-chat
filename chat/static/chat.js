var ws = new WebSocket("ws://127.0.0.1:8888/ws");

ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data)
    var name = data['name']
    var msg = data['msg']
    $('.table > tbody:last').append(
        '<tr><td class="col-md-4"><b>' + name +
        ':</b></td><td class="col-md-8">' + msg +'</td></tr>'
    );
    var n = $(document).height();
    $('html, body').animate({ scrollTop: n });
};

$('#msg_form').submit(function(){
    $massage = $("input[name='msg']")
    var msg = $massage.val()
    $massage.val('');
    ws.send(msg);
    return false;
});