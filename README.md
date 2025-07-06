# 🧠 Deskora — Your Desktop AI Companion

**Deskora** is a privacy-respecting, local virtual assistant designed to run entirely on your machine. Powered by lightweight LLMs like Phi-3 Mini and Python, Deskora can learn, remember, and assist you — all with a charming personality!

> 💻 No cloud. No surveillance. Just you and your personal AI — on your own terms.

---

## 🚀 Features

- 🧠 **LLM-Powered Responses** – Uses `llama-cpp-python` to run open-source GGUF models locally
- 💾 **Long-Term Memory** – Remembers your preferences, facts, and feedback across sessions
- 🧩 **Skill System** – Execute tasks like opening apps or storing information
- 🗂️ **Modular Design** – Easily add new features, skills, and memory extensions
- 🎨 **Personality Engine** – Customize tone, name, emojis, and response style

---

## 📷 Preview (Coming Soon!)

*A little virtual buddy living on your desktop... coming soon!*

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Divyam2806/deskora.git
cd deskora
````

### 2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download an LLM Model (Example: Phi-3 Mini)

> 🧠 Deskora supports GGUF models via `llama-cpp-python`.

Download [Phi-3 Mini (4K, Q4 GGUF)](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-GGUF) and place it in:

```
/models/phi3-mini.gguf
```

*(The `models/` folder is gitignored — you must place the model manually.)*

---

## 🧪 Run Deskora

```bash
python main.py
```

You'll be greeted by Deskora in the terminal. Start chatting!

---

## 🧠 Architecture Overview

```
deskora/
├── assistant/
|   ├── llm.py              # Handles LLM communication and prompting
│   ├── core.py         # Main input/output logic and execution plan
│   ├── skills.py       # Skills like open calculator, browser, etc.
│   ├── planner.py      # Uses LLM to plan actions from input
│   ├── memory.py       # Long-term memory using SQLite (via SQLAlchemy)
│   └── database.py     # Fact storage and user info
├── models/             # GGUF model files (gitignored)
├── main.py             # CLI entry point
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Planned Features

* 🌐 GUI with virtual desktop entity
* 🎤 Voice input/output
* 🪄 Daily reminders and suggestions
* 🔌 Plugin system for new tools
* 🤖 Personality tuning

---

## 🤝 Contributing

Deskora is open-source and welcomes contributors!

1. Fork the repo
2. Create a new branch
3. Submit a pull request 🚀

---

## 📄 License

MIT License — [LICENSE](LICENSE)

---

## 💬 Acknowledgements

* [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
* [Phi-3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-GGUF)
* Inspired by old-school desktop companions and modern LLMs

---

> ✨ Created with love, curiosity, and a little bit of chaos by [@Divyam2806](https://github.com/Divyam2806)



