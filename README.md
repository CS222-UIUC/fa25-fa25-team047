# Code Companion

**Code Companion** is a personalized, AI-powered technical interview preparation platform that helps users practice coding problems through natural conversation. Instead of browsing long problem lists, users describe what they want to practice, receive a custom-generated problem, and solve it in an interactive browser-based IDE with automated test cases—similar to LeetCode, but tailored to the user.

---

## (a) Project Summary / Presentation Introduction

Finding the right coding problem to practice can be overwhelming. Existing platforms provide massive problem banks, but they often lack personalization and guidance. **Code Companion** reimagines interview preparation by starting with a ChatGPT-style conversation. Users describe the topic and difficulty they want, and the platform generates a matching coding problem, complete with edge cases and an integrated coding environment. This makes learning data structures, algorithms, and interview problem-solving more focused, interactive, and efficient.

---

## (b) Technical Architecture

### High-Level Architecture
Code Companion uses a **separated frontend–backend architecture**:

- **Frontend:** React-based web application for user interaction  
- **Backend:** Flask REST API for business logic and AI integration  
- **Browser Runtime:** Pyodide for running Python code directly in the browser  
- **External Services:** OpenAI API for problem generation  

---

### Frontend
- **Languages:** TypeScript, HTML/CSS  
- **Framework:** React 18 + Vite  
- **UI Components:** Radix UI  
- **Responsibilities:**
  - ChatGPT-style conversational interface  
  - In-browser code editor  
  - Display generated problems and test results  
  - Communicate with backend via HTTP requests  

---

### Backend
- **Language:** Python  
- **Framework:** Flask 3  
- **Responsibilities:**
  - Handle API requests from the frontend  
  - Generate coding problems and edge cases using OpenAI  
  - Manage user state and authentication logic  
  - Validate code using automated test cases  
- **Testing:** PyTest  
- **Secrets Management:** `.env` files for API keys  

---

### Browser-Based IDE
- **Pyodide** executes Python code directly in the browser  
- Enables fast feedback without sending raw code execution to the server  

---

### External APIs
- **OpenAI API** for AI-powered problem and edge-case generation  

---

## (c) Reproducible Installation Instructions

### Prerequisites
- Node.js (v18 or later)
- Python (v3.10+)
- `pip`
- An OpenAI API key

### Create a .env file with:
- OPENAI_API_KEY=your_api_key_here

### Run the backend:
- cd flask
- python app.py

### Run the frontend:
- Open a new terminal
- cd ChatBoxUI
- npm install
- npm run dev

## The app will open at
- http://localhost:5000

## (d) Group Members and Roles

### Maya Swaminathan
- Worked on the **frontend and UI design**
- Built user-facing components and layouts

### Raaghav Pillai
- Worked on **authentication and frontend development**
- Helped integrate frontend logic with backend APIs

### Sharngi Biswas
- Worked on **backend logic**
- Implemented **OpenAI API integration**
- Handled parsing, error handling, and frontend–backend communication

### Varnika Jain
- Worked on **backend development and AI integration**
- Assisted with problem generation and system logic

---

## Tech Stack Summary

- **Frontend:** React 18, Vite, TypeScript, HTML/CSS, Radix UI  
- **Backend:** Flask 3, Python, PyTest  
- **IDE:** Pyodide (browser-based Python execution)  
- **APIs:** OpenAI API  
- **Tooling:** `.env` for secrets  

---

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


