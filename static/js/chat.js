const form = document.querySelector(".chat-input");
const input = form.querySelector("input");
const chatBox = document.querySelector(".chat-messages");

form.addEventListener("submit", async function (e) {

    e.preventDefault();

    const message = input.value.trim();

    if (!message) return;

    // User Message
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.textContent = message;
    chatBox.appendChild(userDiv);

    // Clear Input
    input.value = "";

    // Scroll Bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Thinking...
    const thinking = document.createElement("div");
    thinking.className = "message astra";
    thinking.innerHTML = "🤖 ASTRA is thinking...";
    chatBox.appendChild(thinking);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat-api", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        thinking.innerHTML = data.reply;

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    catch (error) {

        thinking.innerHTML = "❌ Something went wrong.";

    }

});