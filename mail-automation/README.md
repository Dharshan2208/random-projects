# Email Automation with AI (Gemini + Groq)
This project automates Gmail tasks using Python + AI:

- Fetch unread Gmail messages
- Summarize emails with **Groq API** (`summarize.py`)
- Classify and auto-sort emails with **Gemini API** (`classify.py`)
- Send you the summarised emails using smtp server (`email_sender.py`)

## 🛠 Setup

1. **Install dependencies**

```bash
pip install python-dotenv requests google-generativeai
```

2. **Create a `.env` file** in the root directory:

```env
EMAIL_USER=your-gmail@gmail.com
EMAIL_PASS=your-app-password
GROQ_API_KEY=your-groq-api-key
GEMINI_API_KEY=your-gemini-api-key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_TO=mail where you want the summarised mail
```

---

## Usage

```bash
python main.py
```

## 💡 Notes

- You **must use an App Password** for Gmail if 2FA is enabled.

- You can change the Gemini model in `gemini.py` if needed.
- You can change the Groq model in `groq.py` if needed.
- Classification folders will be created in your Gmail automatically.

## 🌐 24/7 Hosting Options

To keep your email assistant running automatically in the cloud, you can deploy it on any of the services below :

- [PythonAnywhere](https://www.pythonanywhere.com)
- [Render](https://render.com)
- [Railway](https://railway.app)

## Credits 
- Made by combining many youtube videos and my idea which led to this.