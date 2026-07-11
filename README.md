# JanSeva AI - Hackathon Project

JanSeva AI is an intelligent platform designed to help Indian citizens discover and understand government welfare schemes. Using AI and RAG (Retrieval-Augmented Generation), it matches users to schemes based on their profile and provides an interactive chatbot to answer questions about eligibility, benefits, and required documents.

---

## 🚀 How to Run the Project Locally

This project consists of a **FastAPI Backend** and a **React/Vite Frontend**. You will need two separate terminal windows to run them.

### Step 1: Set up the Environment Variable
Ensure you have your Gemini API key ready. Inside the `server/` directory, there is a `.env` file that contains:
```env
GEMINI_API_KEY=your_api_key_here
```

### Step 2: Start the Backend (FastAPI)
Open your first terminal and navigate to the backend folder:
```bash
cd server
```
Activate the Python virtual environment:
* **Windows:** `.\venv\Scripts\activate`
* **Mac/Linux:** `source venv/bin/activate`

Start the server:
```bash
uvicorn app.main:app --reload
```
*The backend API is now running at `http://localhost:8000`. You can view the API documentation at `http://localhost:8000/docs`.*

### Step 3: Start the Frontend (React + Vite)
Open a **second terminal** and navigate to the frontend folder:
```bash
cd client
```
Install dependencies (if not already installed) and start the Vite development server:
```bash
npm install
npm run dev
```
*The frontend is now running at `http://localhost:5173`.*

---

## 🧪 How to Test the Application

Once both servers are running, open your browser and navigate to **http://localhost:5173**. Follow these steps to test the full flow:

### 1. User Registration & Authentication
* On the Landing Page, click **Get Started**.
* You will be taken to the Login page. Click **Register here** to create a new account.
* Fill in your Name, Email, and Password. (This data is securely hashed and stored in the local SQLite database).

### 2. Profile Setup & Scheme Recommendation
* Once logged in, go to the **Profile** tab on the left sidebar.
* Fill out demographic details (e.g., Age, Income, Category, State) and click **Update Profile**.
* Go back to the **Dashboard**. The system will dynamically display a list of government schemes you are eligible for based on your profile!

### 3. View Scheme Details
* Click **"View Details"** on any scheme card.
* You will be taken to a dedicated page detailing the specific **Eligibility Criteria**, **Financial Benefits**, and **Required Documents**.

### 4. Test the AI Chatbot (RAG System)
* Click the **blue chat bubble icon** in the bottom right corner of the screen.
* Ask the AI a specific question about a scheme. For example:
  * *"What are the documents needed for the Garuda Scheme?"*
  * *"Am I eligible for PM-KISAN?"*
* **How it works:** The AI searches the local ChromaDB vector store (which contains the scheme dataset) to fetch the exact rules and answers your question without hallucinating!

---

## 📊 Database & Dataset Note
* **Relational Database:** User accounts and profiles are stored locally in `server/janseva.db`.
* **AI Knowledge Base:** The dataset of schemes is converted into embeddings and stored in `server/chroma_db`. 
* **Updating Data:** To add new schemes from the CSV dataset, activate the backend virtual environment and run `python seed_from_csv.py`.
