const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userId = JSON.parse(document.getElementById('user-id').textContent);
const history = JSON.parse(document.getElementById('history').textContent);
const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
const chatWindow = document.querySelector('#chat');
const messageInputDom = document.querySelector('#chat-message-input');
const chatSubmitButton = document.querySelector('#chat-message-submit');
const messageForm = document.querySelector('#chat-form');
const errorHelper = document.getElementById('invalid-helper');
const errorBanner = document.getElementById('error');
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';

const chatSocket = new WebSocket(
    wsProtocol
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
    chatWindow.appendChild(createChatBubble(element));
});
let lastElement = chatWindow.querySelector('div.row:last-child');
if (lastElement) {
    lastElement.scrollIntoView(false);
}


// attach message to the textarea
chatSocket.onmessage = function (element) {
    const data = JSON.parse(element.data);
    chatWindow.appendChild(createChatBubble(data));
    let lastElement = chatWindow.querySelector('div.row:last-child');
    if (lastElement) {
        lastElement.scrollIntoView(false);
    }
};


// disconnect from WS
chatSocket.onclose = function(e) {
    errorBanner.style.display = 'block';
    chatWindow.style.height = '75vh';
    messageInputDom.disabled = 'true';
    chatSubmitButton.disabled = 'true';
    console.error('Chat socket closed unexpectedly: ', e);
};


// set focus to message unput
// enable message to be sent by pressing Enter
messageInputDom.focus();
messageInputDom.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {  // enter, return
        e.preventDefault();
        chatSubmitButton.click();
    }
});

// submit fom by click on the send button
chatSubmitButton.addEventListener('click', processForm);


messageForm.addEventListener('submit', processForm);


function processForm(event) {
    event.preventDefault();

    let formData = new FormData();
    const message = messageInputDom.value;

    formData.append('message', message);
    formData.append('sender', userId);
    formData.append('csrfmiddlewaretoken', csrfToken);

    fetch('/chat/send', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then((data) => {
        if (data.valid == false) {
            // add invalid attr to message input
            messageInputDom.setAttribute('aria-invalid', 'true');

            // show validaton error
            // clear previous error messages first
            errorHelper.innerHTML = '';
            data.errors.message.forEach((elem) => {
                errorHelper.appendChild(document.createTextNode(elem))
            })

        }
        else {
            // valid data

            // clear errors first
            messageInputDom.removeAttribute('aria-invalid');
            errorHelper.innerHTML = '';

            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender_id': userId,
            }));

            // delete previous input value
            messageInputDom.value = '';
            chatSubmitButton.disabled = true;
            let lastElement = chatWindow.querySelector('div.row:last-child');
            if (lastElement) {
                lastElement.scrollIntoView(false);
            }
        };
    })
    .catch(error => console.error(error));
}


function createChatBubble(element) {
    let row = document.createElement('div');
    row.classList.add('row');
    row.classList.add(element.sender_id == userId ? 'container-me' : 'container-buddy');

    let bubbleElement = document.createElement('article');
    bubbleElement.className = element.sender_id == userId ? 'me' : 'buddy';
    bubbleElement.appendChild(document.createTextNode(element.message));

    row.appendChild(bubbleElement);
    return row
}
