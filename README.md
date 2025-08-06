## Deskora – Your Personal AI Assistant

**Deskora** is a local-first AI assistant powered by Google’s Gemini API. It can understand and respond to your natural language input, perform actions, store facts, speak replies out loud, and listen to voice commands — all within a stateful conversation.

---

### ✨ Features

* 🔁 Stateful chat with long-term memory
* 🧠 Planner system powered by **Gemini API**
* 🗣️ Voice output using **gTTS**
* 🎙️ Voice input using **SpeechRecognition**
* 💾 SQLite + SQLAlchemy for persistence
* 🧩 Action execution engine for real-world tasks
* ⚙️ Toggle `speaking` and `listening` modes with settings

---

### 🛠️ Tech Stack

| Component    | Tool/Library               |
| ------------ | -------------------------- |
| LLM Backend  | Google Gemini API          |
| Voice Output | gTTS, playsound            |
| Voice Input  | SpeechRecognition, PyAudio |
| Storage      | SQLite + SQLAlchemy        |
| Language     | Python 3.x                 |

---

### 📁 Project Structure

```
assistant/
│
├── core.py              # Main processing logic
├── planner.py           # Gemini prompt planner
├── skills.py            # Executes actions
├── database.py          # DB models and helpers
├── settings.py          # Toggle settings
├── gemini_llm.py 
│
speech/
├── speaker.py           # gTTS-based speaking
├── listener.py          # SpeechRecognition input
│
main.py                  # Main loop
.env                     # API key (should be gitignored)
```

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

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

Ensure `.env` is in `.gitignore` to avoid pushing sensitive data.

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

### 🧪 Example Usage

```bash
python main_cli.py
```

You'll see:

```
Assistant is ready! Type 'exit' to quit.
```

Then speak or type naturally, like:

* "Remind me to drink water every hour"
* "What's the weather today?"
* "Disable listening"

---

### 🛑 Exiting

To exit the assistant, say or type:

```
exit
```


