# Code Companion Project Proposal

## 📢 Pitch
Finding the right coding problem to practice can be overwhelming. Platforms like LeetCode offer massive lists, but users often struggle to find a problem that perfectly matches their desired topic, difficulty, and learning goals. **Code Companion** reimagines this experience by starting with a simple conversation. It's a coding platform that uses a ChatGPT-style interface to help you find the perfect problem, then transitions into a full-featured IDE to help you solve it, and makes learning topics like data structures very personal and interview prep very easy.

---

## ⚙️ Functionality

- Users open up the web application and see a **ChatGPT** interface where it asks what problem they would like to solve
- The user then starts typing a general problem, ex, give me a dynamic programming problem about trees, or give me a prefix-sum problem.
- Then, after the user clicks enter, a **LeetCode** interface pops up with a question generated and edge cases generated.
- Users can **run** their code to see if they pass basic test cases, then the edge cases, just like the LeetCode platform.
- Users can **publish** their questions, along with edge cases.
- A **competition** feature where you are timed against another person in real time and can score points, add friends on the platform, and see what problems your friends are currently attempting.

---

## 🧩 Components

### 🔹 Backend
- **Framework:** Python with the Flask framework
- **Reasoning:** Python's extensive support for AI/ML libraries makes it a natural choice, and Flask's simplicity allows for rapid development of our API. The backend has the following responsibilities
- **Database:** PostgreSQL database to store user data, problem statements, function signatures, and test cases (both public and hidden).
Handle Conversational AI
- **Authentication:** `django-allauth` for OAuth (Slack + Discord)
- **APIs:**  
  - Slack SDK  
  - Python Discord library  
  - OpenAI API (GPT-4)
- **Realtime communication:** WebSockets for sending/receiving live messages
- **Evaluate Submissions and Analyze Complexity** The backend will compare the code's output with the expected results. For complexity analysis, we will implement a static analyzer to provide an estimated Big-O notation based on code structure (e.g., nested loops, recursion).



---

### 🔹 Frontend
- **Language:** TypeScript  
- **Framework:** React  
- **Testing:** React Testing Library  
- **Reasoning:** TypeScript’s type safety prevents runtime bugs; React is the most documented and widely used frontend framework.  

**Responsibilities:**
- Display workspace/server list  
- Display channel list and messages  
- Provide UI for sending messages  
- Handle login & redirects  
- Communicate with backend over HTTP (auth) and WebSocket (chat)

---

### 🔹 Design Choice
We chose a **separated architecture**:
- Django handles backend logic and APIs
- React handles UI and user interactivity  
This allows parallel development (frontend team can mock backend data early).

---

## 🗓️ Weekly Planning

| Week | Dates | Tasks |
|------|--------|-------|
| **1** | Week 1 | Set up Flask server; Create a login/signup page |
| **2** | Week 2| CImplement user authentication endpoints. Populate the database with initial problems. |
| **3** | Week 3 | Build the initial chat interface UI. Set up OpenAI API integration for parsing user requests. |
| **4** | Week 4 | Connect the frontend chat to the backend to fetch and display a selected problem. |
| **5** | Week 5 | Design and build the three-panel IDE layout. Integrate the Monaco Editor component. |
| **6** | Week 6 | Develop the Docker-based code execution sandbox. Create an endpoint to run code against sample tests. |
| **7** | Week 7 | Connect the IDE's "Run" button to the backend sandbox and display output in the frontend console. |
| **8** | Week 8 | Implement the submission logic with hidden edge cases and correctness checks. |
| **9** | Week 9 | Connect the "Submit" button and build UI components to display final results and submission history. |
| **10** | Week 10 | Implement the complexity analyzer. Clean up the codebase, fix bugs, and refine the user experience. Do final quality testing. |

---


