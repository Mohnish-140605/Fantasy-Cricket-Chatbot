# 🏏 Fantasy Cricket Chatbot Assistant

An AI-powered Fantasy Cricket Assistant built using **Streamlit** and **LLMs**, providing intelligent suggestions, real-time match insights, player analysis, fantasy team generation, and fun cricket games like trivia and banter.

---

## ⚙️ Features

- 💬 **Interactive Chatbot**: Get player recommendations, match previews, pitch reports, and live insights through a chat interface.
- 📈 **Player & Match Analytics**: Analyze recent form, pitch conditions, opposition impact, and maximize your fantasy points.
- 🤖 **LLM Integration**: Receive natural-language explanations and responses powered by OpenAI or Hugging Face.
- 🎮 **Gamified Add-ons**:
  - 🧠 Cricket Trivia (Easy, Medium, Hard)
  - 🕵️ Player Guessing Challenge
  - 😂 Banter Mode with different AI personas
- 🧱 **Modular Architecture**: Highly organized, testable, and configurable project layout.

---

## 🗂️ Project Structure

```
fantasy-cricket-assistant/
├── app.py                    # Streamlit app entry point
├── config/                   # Configuration & secrets
├── core/                     # Data access, analytics, chat engine
├── services/                 # LLM integration, caching, notifications
├── features/                 # Team builder, trivia, banter, match analyzer
├── assets/                   # Prompt files, templates, fallback DB
├── utils/                    # Logging, error handling, validation
└── tests/                    # Unit and integration tests
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fantasy-cricket-assistant.git
cd fantasy-cricket-assistant
```

### 2. Create and Activate Virtual Environment

#### On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (Git Bash or PowerShell):

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your API Keys

You need valid API keys to access cricket data and LLM services.

- Open the file: `config/api_keys.py`
- Replace placeholder values with your real API keys:

```python
OPENAI_API_KEY = "your-openai-api-key"
CRICBUZZ_API_KEY = "your-cricbuzz-api-key"
```

> Alternatively, set them as environment variables for better security.

### 5. Run the App

```bash
streamlit run app.py
```

---



## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🙌 Contributions

PRs and feature suggestions are welcome! Please open an issue or fork the project and submit a pull request.

---

## 🛡️ License

This project is licensed under the MIT License.

---

## 📬 Contact

Created by Mohnish G Naidu — mohnishg.bsc23@rvu.edu.in
For collaboration or feedback, feel free to reach out!
