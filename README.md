# YZTA_bootcamp_137

# 📝 1st Sprint Report – MentalTrack

**Sprint Duration:** June 30 – July 6  
**Team:** MentalTrack Development Team  
**Sprint Goal:** Define the core idea, team structure, and technology stack of the project. No coding was planned during this sprint.

---

## ✅ What We Achieved

### 🤝 Team Introduction & Role Sharing
We held our first meetings and got to know each other. Each team member shared their strengths, and preliminary roles were assigned (e.g., frontend, backend, documentation).

### 💡 Project Idea Finalized
We decided to build **MentalTrack**, an AI-powered emotional journal where users speak about their day and receive emotional analysis and personalized feedback from a large language model (LLM).

### 🧠 Problem Definition
Mental health and emotional awareness are often overlooked. MentalTrack aims to help users express their daily emotions through voice and receive meaningful AI feedback in return.

### 🧪 Selected Tech Stack
- **Frontend:** Streamlit (simple, fast deployment)  
- **Speech-to-Text:** Google STT (via SpeechRecognition)  
- **AI Analysis:** Gemini API (Google Generative AI)  
- **Language:** Python  
- **Environment Management:** `.env`, `python-dotenv`  
- **Dependency Management:** `requirements.txt`  

---

## 📅 Daily Scrum Summary
We held daily sync-ups using Google Meet.  
Key discussion points included:
- Clarifying project scope and MVP boundaries  
- Aligning on technology (Streamlit, Gemini, STT)  
- Assigning first tasks for next sprint  

---

## 📌 Sprint Board Updates
We used Trello to track and manage our sprint progress.

**Board Structure:**
- **Backlog:** Feature ideas, inspirations  
- **Sprint 1:** Role sharing, idea discussion, tech stack research  
- **Done:** All sprint 1 goals completed  


## 🔢 Estimated Story Points (Sprint 1)

| Task                         | Story Points |
|------------------------------|--------------|
| Team structure & roles       | 3            |
| Finalize idea                | 5            |
| Define tech stack            | 5            |
| Write report/documentation   | 2            |

**Total Estimated Points:** **15**

---

## 🧠 Estimation Logic
We used **Fibonacci-based story points** to reflect effort and complexity:
- **1:** trivial  
- **3:** small (1 hour)  
- **5:** medium (1–2 hours)  
- **8+:** larger or ambiguous, needs discussion

Since this sprint was planning-focused, all estimations were based on non-coding effort.

---

## ✅ Sprint Deliverables

| Deliverable                   | Status     |
|------------------------------|------------|
| Team roles identified        | ✅ Done     |
| Final project idea selected  | ✅ Done     |
| Problem & solution defined   | ✅ Done     |
| Tech stack listed            | ✅ Done     |
| Codebase initialized         | ❌ Not yet  |
| No development this sprint   | ✅ As planned |

---

## 🔁 Sprint Retrospective

### ✅ What went well:
- Active and respectful communication
- Reaching alignment on vision and roles

### ⚠️ What could improve:
- Idea refinement required multiple iterations
- Coordination was slightly delayed due to different schedules

### 💡 Suggestions for Next Sprint:
- Define GitHub issue templates  
- Encourage async updates to reduce sync load  
- Begin planning for basic UI and microphone integration

---

## 🚀 Goals for Sprint 2
- Set up initial project directory and GitHub repository  
- Implement basic Streamlit UI  
- Integrate microphone input and speech recognition  
- Configure Gemini API key and `.env` environment  
- Generate first AI feedback from sample voice input  

---

## 🔖 Notes
This sprint focused on planning, communication, and scope definition. Although no code was written, a clear foundation was established for development in Sprint 2.

---


# 📝 2nd Sprint Report – MentalTrack

**Sprint Duration:** July 6 – July 20  
**Team:** MentalTrack Development Team  
**Sprint Goal:** Build the initial prototype of the application, focusing on voice input, emotional analysis integration, and basic user interface with Streamlit.

---

## ✅ What We Achieved

### 🎨 Basic Streamlit UI Implemented  
A simple and intuitive UI was created using Streamlit, allowing users to record voice input and view AI-generated feedback.

### 🎙️ Microphone Integration & Voice Capture  
Google Speech Recognition API was integrated successfully. Users can now record their voice within the app interface and have it transcribed.

### 🔐 Environment & API Key Management  
The project was configured to use `.env` files via `python-dotenv` for secure and flexible API key management (Gemini key, etc.).

### 🧠 Gemini API Integration for Emotional Analysis  
We connected the transcribed text to the Gemini LLM API. Initial emotional analysis and feedback generation was tested with mock inputs.

### 💾 Project Directory & GitHub Repository Setup  
The GitHub repository was initialized with the core structure of the application, including `app.py`, `requirements.txt`, and environment configuration.

### 📌 Trello Sprint Board Updates  
The board was updated with Sprint 2 tasks. Progress was tracked through clearly defined "In Progress" and "Done" columns.

---

## 🔢 Estimated Story Points (Sprint 2)

| Task                             | Story Points |
|----------------------------------|--------------|
| Set up GitHub project            | 3            |
| Build basic Streamlit UI         | 5            |
| Microphone input integration     | 5            |
| Speech-to-text functionality     | 5            |
| Gemini API integration           | 8            |
| Test sample AI responses         | 3            |
| Environment configuration (.env) | 2            |

**Total Estimated Points:** 31

---

## 🧠 Estimation Logic

We continued using Fibonacci-based story point estimation. Tasks with external APIs (STT, Gemini) were rated higher due to potential complexity and uncertainty.

---

## ✅ Sprint Deliverables

| Deliverable                 | Status     |
|----------------------------|------------|
| Streamlit UI               | ✅ Done    |
| Microphone input           | ✅ Done    |
| Speech-to-text working     | ✅ Done    |
| Gemini API connected       | ✅ Done    |
| Voice-to-feedback pipeline | ✅ Basic version complete |
| GitHub repo structure      | ✅ Done    |

---

## 🔁 Sprint Retrospective

### ✅ What went well:
- Core components were successfully integrated  
- GitHub workflow improved team collaboration  
- Basic emotional feedback was meaningful

### ⚠️ What could improve:
- Error handling for STT and API calls needs enhancement  
- More test cases needed for various emotional tones

### 💡 Suggestions for Next Sprint:
- Add loading animations and error messages in UI  
- Improve AI feedback formatting  
- Store user feedback locally (SQLite or file-based for MVP)

---

## 🚀 Goals for Sprint 3 (July 20 – August 3)
- Improve feedback quality and tone detection  
- Add sentiment classification (positive, negative, neutral)  
- Store input and feedback as daily logs  
- Add export/download option for user logs  
- Polish UI for better UX



## 📝 3rd Sprint Report – NeuroScan AI (Alzheimer MRI Classification)  
**Sprint Duration:** July 20 – August 3  
**Team:** MentalTrack Development Team  
**Sprint Goal:** Transition the project focus to develop an AI-powered Alzheimer diagnosis system using MRI scans and deliver a working prototype with core features.

---

### ✅ What We Achieved

🔄 **Project Pivot to Alzheimer MRI Classification**  
We shifted our project from MentalTrack emotional journaling to NeuroScan AI, focusing on AI-based Alzheimer detection via MRI images. This pivot was motivated by the team's interest and emerging domain relevance.

🧑‍💻 **User Authentication & Database Management**  
Implemented secure user registration, login, and session state management with SQLite backend.

🧠 **AI Model Integration for MRI Classification**  
Integrated a pretrained ResNet deep learning model that classifies MRI images into Alzheimer stages with ~93% accuracy.

📊 **Report Generation & Storage**  
Developed functionality to generate visual diagnostic reports, save them per user with timestamps, and store file paths in the database.

🕰️ **Historical MRI Report Listing**  
Enabled users to view all their past MRI classification reports with thumbnails and timestamps, improving user experience and follow-up.

---

### 🔢 Estimated Story Points (Sprint 3)

| Task                                    | Story Points |
|-----------------------------------------|--------------|
| Project pivot & planning                 | 5            |
| User authentication & session management| 5            |
| AI model integration & inference        | 8            |
| Report generation & file saving         | 5            |
| Historical report listing UI             | 5            |
| Database schema updates                  | 3            |
| Testing and bug fixes                    | 3            |
| **Total Estimated Points**               | **34**       |

---

### 🔁 Sprint Retrospective

✅ **What went well:**  
- Successful transition to new project focus with clear team alignment  
- Stable implementation of user management and session persistence  
- Accurate AI classification with explainable Grad-CAM visualizations  

⚠️ **What could improve:**  
- Code modularity and documentation could be enhanced  
- Error handling and input validation need strengthening  
- UI responsiveness on various screen sizes  

---

### 🚀 Delivery Summary  
We have delivered a fully functional NeuroScan AI prototype capable of classifying Alzheimer's stages from MRI scans, with user account management and historical report tracking. The system is ready for deployment and user testing.
