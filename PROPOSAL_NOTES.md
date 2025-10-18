# Universal Chat Project Proposal

## 📢 Pitch
Students often use multiple communication platforms for different classes—Slack, Discord, and Microsoft Teams—making it difficult to stay organized.  
**Universal Chat** unifies all these platforms into a single interface, letting users manage all class communications in one place.

---

## ⚙️ Functionality

- Access and send messages through **Slack** and **Discord**
- View all connected **workspaces/servers**
- See available **channels** within each workspace/server
- Browse **past messages**
- Send **new messages**
- Create an account via **email**
- Link **Slack** and **Discord** accounts to that user account

---

## 🧩 Components

### 🔹 Backend
- **Framework:** Python with Django  
- **Reasoning:** Team members already familiar with Python; Django has strong community support and built-in tools
- **Database:** SQLite (built-in Django ORM support)
- **Authentication:** `django-allauth` for OAuth (Slack + Discord)
- **APIs:**  
  - Slack SDK  
  - Python Discord library  
- **Realtime communication:** WebSockets for sending/receiving live messages

**Responsibilities:**
- Manage user accounts  
- Handle OAuth authentication  
- Retrieve and send messages  
- Sync data from multiple chat providers  
- Provide REST and WebSocket endpoints to the frontend  

**Design for Extensibility:**  
Each provider (Slack, Discord, etc.) is wrapped in a standard class interface, so adding new ones later is easy (by subclassing a parent provider class).

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
| **1** | Feb 24 – Feb 28 | Create login page; install authentication libraries for backend |
| **2** | Mar 3 – Mar 7 | Configure Slack + Discord OAuth; redirect to frontend |
| **3** | Mar 10 – Mar 14 | Create homepage; decide on colors/fonts; add frontend redirect handler |
| **(Break)** | Mar 17 – Mar 21 | Spring Break – Trip to Ba Sing Se 🏝️ |
| **4** | Mar 24 – Mar 28 | Create workspace/server list (frontend); backend method for Discord servers |
| **5** | Mar 31 – Apr 4 | Call backend from frontend; backend method for Slack workspaces |
| **6** | Apr 7 – Apr 11 | Create channels list (frontend); backend method for Discord channels |
| **7** | Apr 14 – Apr 18 | Connect frontend to backend channels; backend method for Slack channels |
| **8** | Apr 21 – Apr 25 | Build messages component; support sending messages via Discord |
| **9** | Apr 28 – May 2 | Connect messages component; add Slack messaging support |
| **10** | May 5 – May 9 | Final UX cleanup; refactor code; add buffer for risks |

---

## ⚠️ Potential Risks & Mitigation

| Risk | Description | Impact | Mitigation |
|------|--------------|---------|-------
