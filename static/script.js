


function sendMessage() {
    const message = document.getElementById("message").value;
    const model = document.getElementById("model").value;
    const chatBox = document.getElementById("chat-box");

    if (!message) return;

    chatBox.innerHTML += `<div class="user-msg"><b>You:</b> ${message}</div>`;

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message,
            model: model
        })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `
            <div class="bot-msg">
                <b>Bot:</b> ${data.response}
                <br><small>(${data.response_time}s | ${data.model_used})</small>
            </div>
        `;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    document.getElementById("message").value = "";
}

function clearChat() {
    fetch("/clear", { method: "POST" })
        .then(() => {
            document.getElementById("chat-box").innerHTML = "";
        });
}
