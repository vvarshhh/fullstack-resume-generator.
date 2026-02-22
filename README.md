# AI Resume to Job Email Generator

A full-stack app that extracts your resume, and uses Groq AI to write personalized job application emails. Built with **FastAPI** (backend) and **HTML/CSS/JS** (frontend).

---

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file (copy from `.env.example`):
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com

Start the server:
```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

---

### 2. Frontend Setup

No build step required! Just open `frontend/index.html` in your browser.

Make sure the backend is running before generating emails.

---

### 3. EmailJS Setup (to send emails)

1. Create a free account at https://www.emailjs.com
2. Create an Email Service (Gmail, Outlook, etc.)
3. Create an Email Template with these variables:
   - `{{to_email}}` — recipient
   - `{{subject}}` — email subject
   - `{{message}}` — email body
   - `{{company}}` — company name
   - `{{job_role}}` — job role
4. Enter your **Service ID**, **Template ID**, and **Public Key** into the config panel in the app.

---

## 🛠 Tech Stack

| Layer    | Technology            |
|----------|-----------------------|
| Backend  | Python, FastAPI, Uvicorn |
| PDF Parse | pdfplumber            |
| AI       | Groq (llama-3.3-70b)  |
| Frontend | HTML, CSS, JavaScript |
| Email    | EmailJS               |
