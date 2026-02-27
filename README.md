# Caesar Cipher WhatsApp Bot

WhatsApp bot that encrypts and decrypts messages using the Caesar Cipher algorithm. It consists of two parts that must run simultaneously: a **Python Flask API** that handles the cipher logic, and a **Node.js WhatsApp bot** that receives commands and calls the API.

---

## Requirements

- Python 3.10+
- Node.js 18+

---

## Setup

### 1. Python API

Create and activate a virtual environment, then install dependencies:

```bash
# Create virtual environment
python -m venv env

# Activate (Windows)
env\Scripts\activate

# Activate (macOS/Linux)
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. WhatsApp Bot (Node.js)

```bash
npm install
```

---

## Running

Both processes must run at the same time, each in its own terminal.

**Terminal 1 — Flask API:**

```bash
# Activate the virtual environment first (if not already active)
env\Scripts\activate

python main.py
```

The API will start at `http://127.0.0.1:5000`.

**Terminal 2 — WhatsApp Bot:**

```bash
node index.js
```

On first run, a QR code will appear in the terminal. Scan it with WhatsApp to link the bot.

---

## Bot Commands

| Command                    | Description                         | Example                   |
| -------------------------- | ----------------------------------- | ------------------------- |
| `!cypher <text> <shift>`   | Encrypts a text using Caesar Cipher | `!cypher Hello World 3`   |
| `!decypher <text> <shift>` | Decrypts a text using Caesar Cipher | `!decypher Khoor Zruog 3` |
| `ping`                     | Health check                        | `ping`                    |
| `que`                      | Sends a sticker                     | `so`                      |

> The `alphabet` parameter defaults to English. To use the Spanish alphabet (includes `ñ`), the API accepts `"alphabet": 2` directly via HTTP if needed.

---

## API Endpoints

The Flask API can also be used independently via HTTP.

**POST** `/api/encrypt`  
**POST** `/api/decrypt`

Request body:

```json
{
  "text": "Hello World",
  "shift": 3,
  "alphabet": 1
}
```

- `alphabet`: `1` = English (default), `2` = Spanish

Response:

```json
{
  "result": "Khoor Zruog"
}
```
