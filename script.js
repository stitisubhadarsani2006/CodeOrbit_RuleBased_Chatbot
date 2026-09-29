/*
 * ---------------------------------------------------------------------
 * DECISION LOGIC
 * ---------------------------------------------------------------------
 * No AI model here — just keyword matching checked in a fixed order.
 * Each rule is a set of trigger keywords and a list of candidate
 * replies. The FIRST rule whose keyword appears anywhere in the
 * (lowercased) user message is the one that responds. If nothing
 * matches, and the message doesn't end in "?", we fall back to a
 * generic "I don't understand" reply.
 * ---------------------------------------------------------------------
 */

const RULES = [
  {
    id: "greeting",
    keywords: ["hi", "hello", "hey", "greetings", "good morning", "good evening"],
    responses: [
      "Hello! How can I help you today?",
      "Hi there! What's on your mind?",
      "Hey! Good to see you."
    ]
  },
  {
    id: "farewell",
    keywords: ["bye", "goodbye", "see you", "see ya", "farewell"],
    responses: [
      "Goodbye! Have a great day.",
      "See you later!",
      "Take care!"
    ]
  },
  {
    id: "thanks",
    keywords: ["thanks", "thank you", "appreciate it"],
    responses: [
      "You're welcome!",
      "Happy to help!",
      "Anytime!"
    ]
  },
  {
    id: "wellbeing",
    keywords: ["how are you", "how're you", "how are things"],
    responses: [
      "I'm just a program, but I'm running smoothly! How about you?",
      "Doing well, thanks for asking!"
    ]
  },
  {
    id: "identity",
    keywords: ["your name", "who are you", "what are you"],
    responses: [
      "I'm a simple rule-based chatbot.",
      "Just a small bot that matches keywords to canned replies."
    ]
  },
  {
    id: "help",
    keywords: ["help", "what can you do", "commands"],
    responses: [
      "I can respond to greetings, farewells, thanks, and a few simple questions. Try saying 'hi', asking 'how are you', or asking my name!"
    ]
  }
];

const GENERIC_QUESTION_RESPONSES = [
  "That's an interesting question, but I don't have a specific rule for it."
];

const FALLBACK_RESPONSES = [
  "I'm not sure I understand. Could you rephrase that?",
  "Sorry, I don't have a rule for that yet.",
  "Hmm, I don't know how to respond to that."
];

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Walks the RULES list top to bottom (mirrors an if/elif chain) and
// returns both the reply text and which rule id fired, so the UI can
// highlight the matching entry in the Rulebook panel.
function getResponse(userInput) {
  const text = userInput.toLowerCase().trim();

  for (const rule of RULES) {
    const matched = rule.keywords.some(keyword => text.includes(keyword));
    if (matched) {
      return { reply: pickRandom(rule.responses), ruleId: rule.id };
    }
  }

  // No specific rule matched — check if it's at least a question.
  if (text.includes("?")) {
    return { reply: pickRandom(GENERIC_QUESTION_RESPONSES), ruleId: "question" };
  }

  // Nothing matched at all.
  return { reply: pickRandom(FALLBACK_RESPONSES), ruleId: "fallback" };
}

// ---------------------------------------------------------------------
// UI WIRING
// ---------------------------------------------------------------------
const messagesEl = document.getElementById("messages");
const inputEl = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const ruleItems = document.querySelectorAll(".rule-item");

function addMessage(text, sender, ruleId) {
  const row = document.createElement("div");
  row.className = "msg-row " + sender;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.appendChild(bubble);

  if (sender === "bot" && ruleId) {
    const tag = document.createElement("div");
    tag.className = "rule-tag";
    tag.textContent = "rule matched: " + ruleId;
    row.appendChild(tag);
  }

  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function highlightRule(ruleId) {
  ruleItems.forEach(item => {
    item.classList.toggle("active", item.dataset.rule === ruleId);
  });
}

function handleSend() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, "user");
  inputEl.value = "";

  const { reply, ruleId } = getResponse(text);
  highlightRule(ruleId);

  // Small delay so the reply feels like a response, not an instant echo.
  setTimeout(() => addMessage(reply, "bot", ruleId), 300);
}

sendBtn.addEventListener("click", handleSend);
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") handleSend();
});
