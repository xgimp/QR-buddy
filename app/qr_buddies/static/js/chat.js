const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userId = JSON.parse(document.getElementById('user-id').textContent);
const history = JSON.parse(document.getElementById('history').textContent);
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
// const chatLog = document.querySelector('#chat-log');
const messageInputDom = document.querySelector('#chat-message-input');
const chatSubmitButton = document.querySelector('#chat-message-submit');
const messageForm = document.getElementById('chat-form');
const errorElement = document.getElementById('invalid-helper');

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


// attach chat history entries to the chat element
history.forEach(element => {
    document.querySelector('#chat').appendChild(createChatBubble(element));
});


// attach message to the textarea
chatSocket.onmessage = function (element) {
    const data = JSON.parse(element.data);
    // chatLog.value += ('[' + data.sender + ']:' + data.message + '\n');
    document.querySelector('#chat').appendChild(createChatBubble(data));
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


// submit fom by click on the send button
chatSubmitButton.onclick = processForm;


messageForm.addEventListener('submit', processForm);


function processForm(event) {
    event.preventDefault();

    let formData = new FormData();
    const message = messageInputDom.value;

    formData.append('message', message);
    formData.append('sender', userId);
    formData.append('csrfmiddlewaretoken', csrfToken);

    console.log(formData);

    fetch('/chat/send', {
        method: 'POST',
        body: formData,

    })
    .then(response => response.json())
    .then((data) => {
        // console.log('data');
        // console.log(data);  
        if (data.valid == false) {
            // add invalid attr to message input
            messageInputDom.setAttribute('aria-invalid', 'true');

            // show validaton error
            // clear previous error messages first
            errorElement.innerHTML = '';
            data.errors.message.forEach((elem) => {
                errorElement.appendChild(document.createTextNode(elem))
            })

        }
        else {
            // valid data

            // clear errors first
            messageInputDom.removeAttribute('aria-invalid');
            errorElement.innerHTML = '';

            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender_id': userId,
            }));

            // delete previous input value
            messageInputDom.value = '';
            chatSubmitButton.disabled = true;
        };
    })
    .catch(error => console.error(error));
}


function createChatBubble(element) {
    let row = document.createElement('div')
    row.classList.add('row')
    row.classList.add(element.sender_id == userId ? "conntainer-me" : "container-buddy")

    let bubbleElement = document.createElement('article');
    bubbleElement.className = element.sender_id == userId ? "me" : "buddy";
    bubbleElement.appendChild(document.createTextNode(element.message));

    row.appendChild(bubbleElement);
    return row
}
