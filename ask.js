const API_URL = "https://webai-backend.vercel.app/ask";

const askBtn = document.getElementById("askBtn");
const answerBox = document.getElementById("answerBox");
let selectedText = "";

document.addEventListener("mouseup", (e) => {
  if (e.target === askBtn || answerBox.contains(e.target)) return;
  const text = window.getSelection().toString().trim();
  if (text.length > 3) {
    selectedText = text;
    askBtn.style.left = e.pageX + "px";
    askBtn.style.top = (e.pageY + 10) + "px";
    askBtn.style.display = "block";
  } else {
    askBtn.style.display = "none";
  }
});

askBtn.addEventListener("click", async () => {
  askBtn.style.display = "none";
  answerBox.style.display = "block";
  answerBox.textContent = "Thinking...";
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: selectedText })
    });
    const data = await res.json();
    answerBox.textContent = data.answer || data.error;
  } catch (err) {
    answerBox.textContent = "Could not reach the server.";
  }
});

answerBox.addEventListener("dblclick", () => {
  answerBox.style.display = "none";
});