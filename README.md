# Local SQL Agent with Self-Correcting LLM (Ollama)

This project implements a **local AI agent** that converts natural language questions into SQL queries, executes them on a SQLite database and automatically retries with corrected queries if an error occurs.

The system runs fully offline using **Ollama** and a local LLM (e.g., Llama3 or Phi3).

---

## Features

- Natural language → SQL generation
- Automatic SQL execution on SQLite
- Self-correcting retry loop with error feedback
- Fully local inference (no API keys, no cloud)

---

## Example Queries

```
Mennyi volt az összes bevétel?
Mennyi bevételünk származott Laptop eladásból?
Ki a legtöbbet költő vásárlónk?
```

---

## How It Works

The agent follows a multi-step loop:

1. Receives a natural language question
2. Generates SQL using an LLM
3. Executes the query on SQLite
4. If an error occurs, feeds the error back to the model
5. Retries with a corrected query

This process repeats up to **3 attempts**.

```
User Question → LLM → SQL → SQLite → Error → LLM Retry → Result
```

---

## Why This Is an Agentic System

This project demonstrates an **agentic AI architecture** because the model:
- uses external tools (SQLite)
- observes execution results
- adapts its behavior based on feedback
- and iteratively improves its actions

This reflects real-world autonomous tool-using AI systems.

---

## Project Structure

```
sql-agent/
│
├── main.py        # Contains database setup and agent logic
├── bolt.db        # SQLite database (auto-generated)
```

---

## Database Schema

### vevok (customers)
| Column | Type |
|---|---|
| vevo_id | INTEGER |
| nev | TEXT |
| varos | TEXT |

### eladasok (sales)
| Column | Type |
|---|---|
| id | INTEGER |
| termek | TEXT |
| ar | INTEGER |
| datum | DATE |
| vevo_id | INTEGER |

Relationship:
```
eladasok.vevo_id → vevok.vevo_id
```

---

## Requirements

### Install Ollama

Download and install:
```
https://ollama.com
```

Start Ollama in terminal:
```
ollama serve
```

Pull a model:
```
ollama pull llama3
```

You can also use a smaller model:
```
ollama pull phi3
```

---

## Python Dependencies

```
pip install langchain langchain-ollama
```

---

## Running the Agent

```
python agent.py
```

The script will:
- create and populate the database
- start the SQL agent
- execute example queries

---

## Example Output

```
--- 1. próbálkozás SQL kódja: SELECT SUM(ar) FROM eladasok WHERE termek='Laptop'
Siker! Eredmény: [(700000,)]
```

<img width="512" height="112" alt="agentic AI er 1" src="https://github.com/user-attachments/assets/3de3b593-6648-481d-898d-bff3211ca2c1" />

---

## Technologies Used

- **SQLite** – local database
- **Ollama** – local LLM runtime
- **LangChain Ollama** – Python integration
- **Llama 3 / Phi 3** – language models

---

## Limitations

- SQL generation accuracy depends on the model
- Hungarian prompts may reduce performance compared to English
- Schema must be provided manually in the prompt

---

## Future Improvements

- Automatic schema extraction
- Web interface
- Query result explanation in natural language
- Support for multiple databases

---

## Author

- LinkedIn: www.linkedin.com/in/bence-kupecz-119701305
- GitHub: https://github.com/kupeczbence
