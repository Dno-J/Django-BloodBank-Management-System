# 🩸 Django Blood Bank Management System

This is a web-based Blood Bank Management System built using **Django**. It allows administrators to manage donor registrations and blood requests efficiently while tracking real-time blood availability.

---

## 🌟 Features

- 🔐 Secure Admin Login  
- 🧑‍🦰 Donor Registration with Blood Group, Quantity, and Contact Info  
- 🩸 Blood Request Submission by Hospitals/Patients  
- 📊 Real-time Blood Group Availability Dashboard  
- 📋 Donor & Requester Information View/Delete  
- 🚪 Logout with Session Handling  
- 🌙 Stylish Dark Mode UI with AOS Animations  

---

## 🛠️ Tech Stack

- **Backend:** Django (Python 3)  
- **Frontend:** HTML, Bootstrap 5, CSS, AOS  
- **Database:** SQLite3 (default Django DB)  
- **Version Control:** Git & GitHub  

---

## ⚙️ Setup Instructions

## ✅ Prerequisites

- Python 3.10+ installed  
- Git installed  
- Django installed:
  ```bash
  pip install django
  ```

---

## 🚀 Steps to Run Locally

```bash
# Clone the repository
git clone https://github.com/Dno-J/Django-BloodBank-Management-System.git
cd Django-BloodBank-Management-System

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# Install requirements (if requirements.txt exists)
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

---

## 📁 Project Structure

```
BBMS/
├── blood/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── forms.py
│   └── urls.py
├── BBMS/
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
└── manage.py
```

---

## 📌 Git/GitHub Workflow (Used)

```bash
# Initialize Git
git init

# Create a new branch
git checkout -b main

# Add & commit all files
git add .
git commit -m "Initial commit"

# Set remote and push
git remote add origin https://github.com/your-username/Django-BloodBank-Management-System.git
git push -u origin main

# Create .gitignore (PowerShell Safe)
notepad .gitignore  # Add: __pycache__/, *.pyc, *.sqlite3, .env, etc.

# Commit .gitignore
git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## 🧠 Future Improvements

- Email/SMS notifications to donors  
- Filtering/searching donors by location/blood type  
- Export reports to PDF/CSV  
- Auto-matching donors to urgent requests  
- REST API for mobile app integration  

---

Dino Jackson  
📧 [jacksondino00@gmail.com]  
🌐 [www.linkedin.com/in/dino-jackson-486840368]
