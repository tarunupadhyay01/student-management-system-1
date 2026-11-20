# Student Management System

A beginner-friendly full-stack Student Management System built with **Python Flask**, **SQLite**, HTML, CSS and JavaScript.

## Features
- Add, view, edit and delete student records (CRUD)
- Search by student name, email or course
- Dashboard summary cards
- Responsive layout for desktop and mobile
- SQLite database created automatically on first run
- Basic validation and duplicate-email handling

## Requirements
- Python 3.9+
- pip

## Setup (Windows PowerShell)
1. Extract the ZIP file.
2. Open the extracted `Student_Management_System` folder in VS Code.
3. Open the terminal in that folder.
4. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
5. Activate it:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```
6. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
7. Run the application:
   ```powershell
   python app.py
   ```
8. Open **http://127.0.0.1:5000** in your browser.

## Project structure
```text
Student_Management_System/
├── app.py
├── requirements.txt
├── README.md
├── students.db          # created automatically when app starts
├── templates/
│   ├── base.html
│   ├── index.html
│   └── form.html
└── static/
    ├── style.css
    └── script.js
```

## Before publishing to GitHub
- Test add, edit, delete and search.
- Do not upload your virtual environment (`venv/`) or personal data.
- For a production deployment, set a strong secret key, disable Flask debug mode and add authentication/authorization.
