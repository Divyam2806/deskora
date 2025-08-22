## Deskora – Your Personal AI Assistant

**Deskora** is a local-first AI assistant powered by Google’s Gemini API. It can understand and respond to your natural language input, perform actions, store facts, speak replies out loud, and listen to voice commands — all within a stateful conversation.

---

### ✨ Features

* 🔁 Stateful chat with long-term memory
* 🧠 Planner system powered by **Gemini API**
* 🗣️ Voice output using **gTTS**
* 🎙️ Voice input using **SpeechRecognition**
* 💾 SQLAlchemy for persistence
* 🧩 Action execution engine for real-world tasks
* ⚙️ Toggle `speaking` and `listening` modes with settings
* 🖥️ Two modes of interaction: **CLI** or **Desktop Pet GUI**

---

### 🛠️ Tech Stack

| Component    | Tool/Library               |
| ------------ | -------------------------- |
| LLM Backend  | Google Gemini API          |
| Voice Output | gTTS, playsound            |
| Voice Input  | SpeechRecognition, PyAudio |
| Storage      | SQLAlchemy                 |
| GUI (Pet)    | PyQt6, Pillow              |
| Language     | Python 3.x                 |

---

### 🚀 Getting Started

#### 1. Clone the repository

```bash
git clone https://github.com/your-username/deskora.git
cd deskora
```

#### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Add your Gemini API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Ensure `.env` is in `.gitignore` to avoid pushing sensitive data.

---

### 🖥️ Running Deskora

Deskora can run in **two modes**:

#### 1. CLI Mode (Terminal-based)

Run:

```bash
python main_cli.py
```

You’ll see:

```
Assistant is ready! Type 'exit' to quit.
```

Then type naturally, like:

* "Remind me to drink water every hour"
* "What's the weather today?"
* "Disable listening"

---

#### 2. Pet Mode (GUI Desktop Entity)

Run:

```bash
python pet/pet_main.py
```

This launches **Deskora Entity**, a floating, animated character on your desktop.
You can interact with it by:

* **Right-clicking** → Open the prompt window
* **Typing a query** → Entity will respond in a speech bubble
* **Dragging** → Move the entity around your screen

---

### 🗣️ Voice Features

Deskora can both **speak** and **listen**. You can toggle these features at runtime:

| Command             | Effect                 |
| ------------------- | ---------------------- |
| `enable speaking`   | Enable voice output    |
| `disable speaking`  | Mute voice output      |
| `enable listening`  | Start using microphone |
| `disable listening` | Use keyboard only      |

---

### 🧠 Memory & Summarization

Deskora maintains state using conversation history. When the chat history grows too long, it:

* Automatically summarizes previous messages (excluding the initial instruction prompt)
* Sends the summary + latest messages to Gemini to stay within token limits

---

### 🛑 Exiting

To exit Deskora:

* In **CLI mode** → Type: `exit`
* In **Pet mode** → Close the entity window or type `exit` in the prompt
