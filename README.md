# 💰 EBS Tracker (Expense, Budget & Savings)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=black)](https://render.com/)

**EBS Tracker** is a robust, full-stack personal finance application designed to help users track income, manage expenses, set monthly budgets, and visualize savings goals. Built with a Python Flask backend and a MongoDB Cloud database, it features a modern, responsive UI with Dark Mode support and 3D interactive elements.

---

## 🚀 Live Demo
### [Click here to view the Live Application](https://ebs-tracker.onrender.com)
*(Note: If the app sleeps on free tier, please wait 30 seconds for it to wake up)*

---

## ✨ Key Features

*   **📊 Interactive Dashboard:** Real-time KPIs for Income, Expenses, and Balance.
*   **📉 Data Visualization:** Dynamic Chart.js doughnut charts for category breakdowns.
*   **💰 Budget Management:** Set monthly limits and track progress with visual bars.
*   **🎯 Savings Goals:** Create specific goals (e.g., "New Laptop") and track contributions.
*   **📝 CRUD Transactions:** Full Create, Read, Update, Delete functionality for logs.
*   **🌓 Theme System:** Persistent Dark/Light mode stored in local user configs.
*   **📂 Data Export & Import:** 
    *   Generate **PDF Reports** for monthly summaries.
    *   Export data to **CSV**.
    *   **Backup & Restore** entire database via JSON.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python, Flask (MVC Pattern) |
| **Database** | MongoDB Atlas (Cloud) |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Jinja2 Templates |
| **Scripting** | JavaScript (Chart.js for analytics) |
| **Deployment** | Render (Web Service) |
| **File Handling** | FPDF (PDF generation), JSON, CSV |

---

## 📂 Project Structure Explained

Here is a detailed breakdown of the codebase:

```text
EBS_TRACKER/
│
├── app.py                # 🧠 The Brain. Contains all Flask Routes, Controllers, and Logic.
├── db_helper.py          # 🔌 Database Connector. Handles MongoDB initialization and ID conversion.
├── file_handler.py       # 📄 File Logic. Separated logic for generating PDFs, CSVs, and Logs.
├── requirements.txt      # 📦 Dependencies. List of all Python libraries used.
├── Procfile              # ⚙️ Deployment. Tells Render how to run the app (using Gunicorn).
├── user_config.json      # ⚙️ Local Config. Stores user theme preference and currency symbol.
│
├── templates/            # 🎨 HTML Views (Jinja2)
│   ├── base.html         # Master Layout (Sidebar, Navbar, Scripts).
│   ├── dashboard.html    # Main page with Charts, KPIs, and Budget bars.
│   ├── transactions.html # Table view for adding/editing/deleting entries.
│   ├── manage_data.html  # Settings for Categories, Budgets, and Backup/Restore.
│   └── settings.html     # User preferences (Theme/Currency).
│
└── static/               # 💅 Static Assets
    ├── css/
    │   └── style.css     # Custom Styling (Glassmorphism, 3D Cards, Animations).
    └── js/
        └── script.js     # Frontend logic (Toggles, Date handling).


 📸 Results & UI Tour

 1. The Dashboard
A central hub showing financial health at a glance.
![Dashboard View](screenshots/dashboard.png)

 2. Transaction Management
Clean interface to add expenses with category validation.
![Transactions View](screenshots/transactions.png)

 3. Dark Mode
Fully supported dark theme for night-time usage.
![Dark Mode View](screenshots/darkmode.png)

💻 Local Installation Guide
Want to run this locally on your machine? Follow these steps:

1. Clone the Repository

Bash

git clone https://github.com/YOUR_USERNAME/EBS-Tracker.git
cd EBS-Tracker
2. Create Virtual Environment

Bash

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install Dependencies

Bash

pip install -r requirements.txt
4. Configure MongoDB

Set up a MongoDB Atlas Cluster.
Replace the MONGO_URI in app.py with your connection string.
5. Run the App

Bash

python app.py
Visit http://127.0.0.1:5000 in your browser.

🤝 Contributing
Contributions are welcome!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m "Add some AmazingFeature")
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
📝 License
Distributed under the MIT License. See LICENSE for more information.



👤 Author
Mohd Sufyan Khan
https://github.com/sufyankhan1127
