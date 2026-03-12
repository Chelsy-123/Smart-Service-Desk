# Smart Service Desk – AI Powered Helpdesk

Smart Service Desk is an AI-powered helpdesk platform that integrates a Retrieval-Augmented Generation (RAG) chatbot with a ticketing system.
It allows users to resolve issues instantly through AI assistance or create support tickets that are handled by support agents.

The system provides role-based dashboards for **Users, Agents, and Admins**, enabling efficient issue resolution and support management.

---

## Features

* AI-powered chatbot for instant troubleshooting
* Retrieval-Augmented Generation (RAG) based knowledge retrieval
* Create and manage support tickets
* Role-based access control (User / Agent / Admin)
* Agents can view and manage assigned tickets
* Admin panel for managing agents and FAQs
* Knowledge Base document upload for AI retrieval
* FAQ management system
* Automatic email notifications for ticket updates
* Clean dashboard interface with role-based cards

---

## Tech Stack

### Frontend

* React
* Vite
* Bootstrap
* Axios
* React Router

### Backend

* Django
* Django REST Framework

### AI

* Retrieval-Augmented Generation (RAG)

### Notifications & Background Tasks

* Celery
* Redis

### Containerization

* Docker

---

## System Architecture

User → React Frontend → Django REST API → RAG AI Engine → Knowledge Base

Workflow:

1. User interacts with the chatbot
2. The chatbot retrieves relevant information from the knowledge base
3. If the issue is unresolved, the chatbot suggests creating a support ticket
4. Tickets are assigned to support agents
5. Agents resolve the issue and update the ticket
6. Email notifications inform users about ticket updates

---

## Project Structure

Smart-Service-Desk
│
├── backend
│   ├── auth_api        # Authentication APIs
│   ├── chatbot         # Chatbot logic
│   ├── common          # Shared backend utilities
│   ├── config          # Django project settings
│   ├── kb              # Knowledge base management
│   ├── notifications   # Email and background notifications
│   ├── rag             # Retrieval-Augmented Generation logic
│   ├── tickets         # Ticket management system
│   ├── users           # User management
│   └── manage.py
│
├── service-desk-frontend
│   ├── public
│   ├── src
│   │   ├── api         # API request handlers
│   │   ├── components
│   │   │   ├── chatbot
│   │   │   ├── common
│   │   │   ├── dashboard
│   │   │   ├── faq
│   │   │   └── tickets
│   │   │
│   │   ├── context     # Global state management
│   │   ├── hooks       # Custom React hooks
│   │   └── pages       # Application pages
│   │
│   └── package.json
│
├── docs
│   └── screenshots
│
└── README.md

README.md

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Chelsy-123/Smart-Service-Desk.git
cd Smart-Service-Desk
```

---

### Backend Setup

```bash
cd backend

python -m venv myvenv
myvenv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### Frontend Setup

```bash
cd service-desk-frontend

npm install

npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## Screenshots

### Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### AI Chatbot

![Chatbot](docs/screenshots/chatbot.png)

### Ticket Management

![Tickets](docs/screenshots/tickets.png)

---

## Author

Chelsy Thomas
B.Tech Computer Science

---

## License

This project is for educational and portfolio purposes.
