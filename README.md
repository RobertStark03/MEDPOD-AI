# ✚ MedPod-AI

### AI-Assisted Emergency Triage & Supply Chain Resilience Platform

**MedPod-AI** is a full-stack healthcare technology prototype that combines Generative AI-powered emergency triage with supply-chain resource monitoring. It analyzes emergency incident reports, identifies potentially required resources and checks their availability against a demonstration inventory.

**Hackathon Track:** Smart Health & Supply Chain Resilience

---



## 🚨 The Problem

During emergencies, identifying the required medical resources and determining their availability can be challenging. Delays in assessing resource requirements and identifying shortages can complicate emergency response planning.

MedPod-AI explores how AI-assisted incident assessment and resource availability monitoring can be brought together in a single platform.



## 💡 The Solution

MedPod-AI uses Google's Gemini API to analyze emergency incident descriptions and generate structured triage reports. Its supply-chain module compares AI-identified resources against a demonstration inventory and highlights potential shortages.



### Core Workflow

```text
Emergency Incident
        |
        v
  Incident Intake
        |
        v
   Gemini AI Triage
        |
        v
 Resource Identification
        |
        v
 Inventory Matching
        |
        v
 Availability Analysis
        |
        v
 Emergency Response Report
```




## ✨ Key Features

### 🧠 AI-Assisted Emergency Triage

* Gemini-powered analysis of emergency incident descriptions.
* AI-assessed severity classification.
* Identification of potential injuries and concerns.
* Emergency resource recommendations.
* Suggested response actions.
* Structured JSON responses.

### 📦 Supply Chain Resilience Engine

* Resource-to-inventory matching.
* Identification of available resources.
* Low-stock alerts for limited inventory.
* Detection of resources without an inventory match.
* Resource availability summaries.

### 📊 Interactive Emergency Dashboard

* Emergency incident intake form.
* Incident location and affected-person fields.
* AI-generated triage results.
* Resource availability monitoring.
* Responsive web interface.
* Automatic scrolling to generated reports.

### 📄 Automated PDF Reports

* Downloadable emergency assessment reports.
* Structured incident and resource information.
* Browser-based printing and saving.

### 🔐 Secure API Configuration

* Environment-based API key management.
* No hardcoded API credentials.
* `.env` excluded from version control.



## 🏗️ Technology Stack

| Component       | Technology              |
| --------------- | ----------------------- |
| Backend         | Python                  |
| Web Framework   | Flask                   |
| Generative AI   | Google Gemini API       |
| AI SDK          | google-genai            |
| Frontend        | HTML5, CSS3, JavaScript |
| Configuration   | python-dotenv           |
| PDF Generation  | ReportLab               |
| API             | Flask HTTP endpoints    |
| Version Control | Git and GitHub          |



## 📁 Project Structure

```text
medpod-ai-triage/
│
├── app.py
├── test.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
└── venv/              # Local environment; not committed
```



### File Description

* **app.py:** Main Flask application, Gemini integration, triage processing, inventory matching, web interface and PDF generation.
* **test.py:** API testing utility used during development.
* **requirements.txt:** Python dependencies.
* **README.md:** Project documentation and setup instructions.
* **.env.example:** Example environment configuration without private credentials.
* **.gitignore:** Excludes secrets, virtual environments and generated files.



## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd medpod-ai-triage
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API

Copy `.env.example` to `.env`.

**Windows:**

```powershell
copy .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Open `.env` and add your own Gemini API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODELS=gemini-3.5-flash
```

Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

Never commit your actual `.env` file to GitHub.

### 5. Run the application

```bash
python app.py
```

Open the application in your browser:

**http://127.0.0.1:5000**



## 🧪 Example Workflow

**Example synthetic incident:**

```text
A patient is experiencing severe chest pain
and difficulty breathing.
```

The application generates an AI-assisted report containing:

1. Severity assessment.
2. Potential medical concerns.
3. Suggested emergency resources.
4. Suggested response action.
5. Inventory availability checks.
6. A downloadable PDF report.

### Example Supply Availability Analysis

| Resource              | Demonstration Stock | Status    |
| --------------------- | ------------------: | --------- |
| Tourniquets           |            12 units | Available |
| Haemostatic dressings |             3 packs | Low stock |
| IV fluid kits         |             20 kits | Available |
| Oxygen kits           |              2 kits | Low stock |
| Trauma dressing kits  |              8 kits | Available |
| Burn care kits        |              5 kits | Available |

The application compares AI-suggested resources with this inventory and displays the corresponding availability status.



## 📦 Supply Chain Resilience

The supply-chain module demonstrates how AI-generated resource requirements can be connected to inventory availability.

Its current capabilities include:

* Matching requested resources against inventory items.
* Identifying potential stock shortages.
* Reporting resources that have no inventory match.
* Presenting resource availability alongside the AI-generated assessment.

The current inventory is **simulated and hardcoded**. It is not connected to a real hospital, warehouse or procurement system.



### Potential Future Extensions

* Real-time hospital inventory integration.
* Multi-hospital resource visibility.
* Live stock synchronization.
* Automated replenishment alerts.
* Geographic resource mapping.
* Procurement system integration.
* Resource demand forecasting.
* Emergency dispatch integration.



## 🔭 Future Improvements

* Database-backed inventory management.
* Real-time inventory updates.
* User authentication and role-based access control.
* Incident history and analytics.
* Geographic resource visualization.
* Human-reviewed clinical workflows.
* Integration with external healthcare systems.
* Improved resource demand prediction.



## 🛡️ Safety and Responsible AI

MedPod-AI is an experimental hackathon prototype and has not been clinically validated.

* It is not a medical device or a diagnostic system.
* AI-generated assessments may be inaccurate.
* It does not authorize treatment or emergency dispatch.
* Its inventory is simulated, not live.
* AI-generated information requires qualified human review.

Do not enter identifiable patient information into the demonstration application. For a real medical emergency, contact local emergency services immediately.



## 🔒 Security

API credentials are loaded through environment variables.

The following files and directories must not be committed:

```text
.env
venv/
__pycache__/
*.pyc
```

The repository includes `.env.example` so that developers can configure their own API credentials.



## 🎯 Project Objective

MedPod-AI explores the intersection of Generative AI and supply-chain resilience in emergency response planning.

By connecting incident assessment, resource identification and inventory availability in one application, the project demonstrates a potential approach to more informed emergency resource planning.



## 👨‍💻 Developer

**Tusshar Chakraborty**
Computer Science Graduate | AI/ML | Software Engineering | Full Stack Developer

Interests:

* Artificial Intelligence and Machine Learning
* Software Engineering
* Cloud Computing
* Cybersecurity
* Web Developer



## 📜 License

This project is intended for educational, research and hackathon demonstration purposes.

---

<p align="center">
  <strong>✚ MedPod-AI</strong><br>
  AI-assisted emergency intelligence for resource-aware response.
</p>
