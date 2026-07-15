# MediCoreAPI

FastAPI backend for MediCore.

## Project structure

```
MediCoreAPI/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── dependencies/
│   ├── utils/
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```
