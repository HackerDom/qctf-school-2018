BOT_NAME = '8R4!N-1337';
USER_NAME = 'qctf';

function buildMessage(name, text) {
    message = document.createElement('div');
    message.setAttribute('class', 'message');
    
    author = document.createElement('span');
    author.setAttribute('class', 'author');
    author.innerHTML = name;

    content = document.createElement('span');
    content.setAttribute('class', 'content');
    content.innerHTML = text;

    message.appendChild(author);
    message.appendChild(content);

    return message;
}

function addMessage(name, text) {
    message = buildMessage(name, text);
    document.getElementById('chatArea').appendChild(message);
}

function sendMessage() {
    element = document.getElementById('userMessage');
    text = element.innerHTML
    element.innerHTML = ''

    addMessage(USER_NAME, text);
    processMessage(text.trim());
}

function startMessaging() {
    addMessage(BOT_NAME, 'h3ll0, hum4n!!1<br>ΛΛy n4m3 1s 8R4!N-1337');
    addMessage(BOT_NAME, '4v4i1abl3 c0mM4nDs:<br>- /help<br>- /flag<br>- /action');
}

function processMessage(message) {
    switch (message) {
        case '/flag':
            addMessage(BOT_NAME, '50rry i7’s n0t so 345y. 7ry ag41n…');
            break;
        case '/help':
            addMessage(BOT_NAME, 'l1st 0f 4ct1on5:<br>- vvr!73 7h3 ffL46<br>- will be continued...');
            break;
        case '/action vvr!73 7h3 ffL46':
            addMessage(BOT_NAME, 'g00d jo8!!11 y0vr fl4g i5 ' + decodeFlag(message.substr(8)));
            break;
        default:
            addMessage(BOT_NAME, 's0rrY, 1 c4n no7 unD3rsT4nd y00u');
            break;
    }
}

function decodeFlag(message) {
    message = message.split('').reverse().join('\x1b');
    
    ord = [];
    for (var char in message) {
        ord.push(message.charCodeAt(char));
    }

    result = [];
    for (var i = 0; i < ord.length; i++)
        result.push(String.fromCharCode((ord[i] ^ secret[i]) - 1));

    return result.join('');
}
