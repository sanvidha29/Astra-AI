console.log("Voice JS Loaded");

const mic = document.getElementById("micButton");
const status = document.getElementById("status");
const replyBox = document.getElementById("replyBox");

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (!SpeechRecognition) {

    status.innerText =
        "Speech Recognition is not supported in this browser.";

} else {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    mic.addEventListener("click", () => {

        recognition.start();

        mic.classList.add("listening");

        status.innerText = "Listening...";

    });

    recognition.onresult = async function(event){

        const text = event.results[0][0].transcript;

        status.innerText = "You said: " + text;

        mic.classList.remove("listening");

        replyBox.style.display = "block";
        replyBox.innerHTML = "🤖 ASTRA is thinking...";

        try{

            const response = await fetch("/voice-chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    message: text

                })

            });

            const data = await response.json();

            replyBox.innerHTML = data.reply;

            // ASTRA speaks

            const speech = new SpeechSynthesisUtterance(data.reply);

            speech.lang = "en-US";

            speech.rate = 1;

            speech.pitch = 1;

            window.speechSynthesis.cancel();

            window.speechSynthesis.speak(speech);

        }

        catch(error){

            console.error(error);

            replyBox.innerHTML =
                "❌ Unable to connect to ASTRA AI.";

        }

    };

    recognition.onerror = function(event){

        console.log(event.error);

        status.innerText = "Couldn't hear you.";

        mic.classList.remove("listening");

    };

    recognition.onend = function(){

        mic.classList.remove("listening");

    };

}