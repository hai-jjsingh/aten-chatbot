const chat = document.getElementById("chat");
const emptyState = document.getElementById("empty-state");
const form = document.getElementById("composer-form");
const input = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");
const themeToggle = document.getElementById("theme-toggle");

themeToggle.addEventListener("click", () => {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
});

function scrollToBottom() {
  chat.scrollTop = chat.scrollHeight;
}

function removeEmptyState() {
  if (emptyState) {
    emptyState.remove();
  }
}

function addMessage(role, contentHtml) {
  const message = document.createElement("div");
  message.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "👤" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = contentHtml;

  message.appendChild(avatar);
  message.appendChild(bubble);
  chat.appendChild(message);
  scrollToBottom();

  return bubble;
}

function addTypingIndicator() {
  const bubble = addMessage("assistant", "");
  bubble.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;
  return bubble;
}

// Collapse duplicate document/page pairs into a sorted, unique chip list.
function formatSources(sources) {
  if (!Array.isArray(sources) || sources.length === 0) {
    return "";
  }

  const byDocument = new Map();

  for (const source of sources) {
    const docName = source.document_name || "Unknown document";
    const page = source.page_number;

    if (!byDocument.has(docName)) {
      byDocument.set(docName, new Set());
    }
    if (page !== undefined && page !== null) {
      byDocument.get(docName).add(page);
    }
  }

  const chips = [];
  for (const [docName, pages] of byDocument) {
    const sortedPages = [...pages].sort((a, b) => a - b);
    const pageLabel = sortedPages.length
      ? `p. ${sortedPages.join(", ")}`
      : "";
    chips.push(
      `<span class="source-chip"><span class="doc-icon">📄</span>${escapeHtml(
        docName.replace(/_/g, " ")
      )}${pageLabel ? ` · ${pageLabel}` : ""}</span>`
    );
  }

  return `<div class="sources">${chips.join("")}</div>`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function askQuestion(question) {
  removeEmptyState();
  addMessage("user", escapeHtml(question));

  const typingBubble = addTypingIndicator();

  try {
    const response = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await response.json();

    if (!response.ok) {
      typingBubble.innerHTML = `<span class="error-text">${escapeHtml(
        data.error || "Something went wrong."
      )}</span>`;
      return;
    }

    const answerHtml = marked.parse(data.answer || "");
    typingBubble.innerHTML = answerHtml + formatSources(data.sources);
  } catch (err) {
    typingBubble.innerHTML = `<span class="error-text">Failed to reach the assistant. Please try again.</span>`;
  } finally {
    scrollToBottom();
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const question = input.value.trim();
  if (!question) {
    return;
  }

  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  askQuestion(question).finally(() => {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  });
});
