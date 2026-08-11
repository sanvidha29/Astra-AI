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

        mic.classList.remove("speaking");
        mic.classList.add("listening");

        status.innerText = "🎤 Listening...";

    });

    recognition.onresult = async function(event){

        const text = event.results[0][0].transcript;

        mic.classList.remove("listening");

        status.innerText = "🤖 ASTRA is thinking...";

        replyBox.style.display = "block";
        replyBox.innerHTML = "Thinking...";

        try{

            const response = await fetch("/voice-chat",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    message:text

                })

            });

            const data = await response.json();

            replyBox.innerHTML = data.reply;

            status.innerText = "🗣️ ASTRA is speaking...";

            mic.classList.add("speaking");

            const speech = new SpeechSynthesisUtterance(data.reply);

            speech.lang = "en-US";
            speech.rate = 1;
            speech.pitch = 1;

            speech.onend = () => {

                mic.classList.remove("speaking");

                status.innerText =
                    "Tap the ASTRA Orb to start listening";

            };

            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(speech);

        }

        catch(error){

            console.error(error);

            mic.classList.remove("speaking");

            status.innerText = "❌ Connection Failed";

            replyBox.innerHTML =
                "Unable to connect to ASTRA AI.";

        }

    };

    recognition.onerror = function(event){

        console.log(event.error);

        mic.classList.remove("listening");

        status.innerText =
            "Couldn't hear you. Please try again.";

    };

    recognition.onend = function(){

        mic.classList.remove("listening");

    };

}