const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userId = JSON.parse(document.getElementById('user-id').textContent);
const history = JSON.parse(document.getElementById('history').textContent);

const chatLog = document.querySelector('#chat-log');
const messageInputDom = document.querySelector('#chat-message-input');
const chatSubmitButton = document.querySelector('#chat-message-submit');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
    + userId
    + '/'
);


// enable send button if input is not empty
messageInputDom.addEventListener('input', (event) => {
    chatSubmitButton.disabled = true;
    if (
        !(
            event.target.value == '' ||
            event.target.value == this.defaultValue ||
            !event.target.value.replace(/\s/g, '').length
        )
    ) {
        chatSubmitButton.disabled = false;
    }
})


// attach chat history entries to the textarea
chatLog.value = ''
history.forEach(element => {
    chatLog.value += ('[' + element.sender_id + ']:' + element.message + '\n');
});


// attach message to the textarea
chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    chatLog.value += ('[' + data.sender + ']:' + data.message + '\n');
};

// disconnect from WS
chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

// set focus to message unput
// enable message to be sent by pressing Enter
messageInputDom.focus();
messageInputDom.onkeyup = function (e) {
    if (e.key === 'Enter') {  // enter, return
        chatSubmitButton.click();
    }
};

// submit data
chatSubmitButton.onclick = function (e) {

    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'sender': userId,
    }));
    messageInputDom.value = '';
    chatSubmitButton.disabled = true;
};
