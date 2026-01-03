# 🏥 Patient Management System (FastAPI + Streamlit)

Developed by **Daim Qureshi**, this project is a full-stack web application designed to manage patient records efficiently. It uses a **FastAPI** backend for data processing and a **Streamlit** frontend for a user-friendly interface.

## 🚀 Features
- **FastAPI Backend:** Handles API requests, Pydantic data validation, and custom domain checks.
- **Streamlit Frontend:** A clean dashboard to view, add, search, and delete patients.
- **JSON Persistence:** All data is permanently saved in a `patients.json` file.
- **Health Analytics:** Automatically calculates **BMI** and provides a health **Verdict** (Normal, Overweight, etc.).
- **Interactive API Docs:** Built-in Swagger UI for testing endpoints.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Frontend:** Streamlit, Requests, Pandas
- **Storage:** JSON

## 📂 Project Structure
```text
├── main_fastapi.py     # Backend API logic
├── app_streamlit.py    # Frontend UI logic
├── patients.json       # Database (JSON format)
└── README.md           # Project documentation
