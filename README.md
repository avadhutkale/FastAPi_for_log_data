# 🚀 FastAPI Log Parser API

This project provides a simple RESTful API using **FastAPI** to parse and analyze server/application log files from a local `logs/` directory. It exposes endpoints to filter, query, and retrieve statistics on log entries.

---

## 📁 Project Structure
FastAPi_for_log_data/
├── d.py # Contains parse_log_line() to split log lines into components
├── main.py # FastAPI application with endpoints for log access and analysis
├── logs/ # Folder containing .log files to be parsed (can include sample logs)
├── .gitignore
└── README.md

---

## 📜 Sample Log Format

The log files are expected to have entries in the following format:


Each line must contain:
- Timestamp
- Log level (INFO, WARNING, ERROR, etc.)
- Component name
- Message

---

## ⚙️ How It Works

- On app startup, all `.log` files inside the `logs/` directory are read and parsed.
- Each line is split into: `timestamp`, `level`, `component`, and `message`.
- All parsed entries are stored in memory as a list of `LogEntry` objects.

---

## 🧪 API Endpoints

### `GET /logs`
Retrieve logs, with optional filters:

### `GET /logs/{log_id}`
Retrieve a single log entry by its UUID.

### `GET /logs/stats`
Returns:

Total number of log entries
Count by log level
Count by component

▶️ Run the API Locally
1) Install dependencies:
    pip install fastapi uvicorn
2) Run the server:
     uvicorn main:app --reload

