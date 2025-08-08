## 📖 Description

 Telegram bot game that presents you with a quote and challenges you to determine whether it was said by **Fyodor Dostoevsky** or a fictional **Toxic Twitter User**.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mattveeye/Dostoevsky-or-Toxic-Bot

cd Dostoevsky-or-Toxic-Bot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: .\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 Setup

### 1. Create a `.env` File

Create a `.env` file in the root directory of the project.

### 2. Add Your Bot Token

```env
BOT_TOKEN=<your_telegram_bot_token_here>
```


---

## ▶️ Running the Bot

1. Activate the virtual environment:

```bash
# On Linux: source venv/bin/activate   # On Windows: .\venv\Scripts\activate
```

2. Start the bot:

```bash
python main.py    or    python3 main.py
```

Your bot should now be online and responding on Telegram.

---

## 🎮 Bot Commands

| Command       | Description |
|---------------|-------------|
| `/start`      | Start the game and receive a welcome message |
| `/stats`      | View your current session statistics |
| **Start Game** | Begin a new round |
| **Dostoevsky** / **Toxic Guy** | Choose who you think said the quote |
| **Give Up**   | Reveal the correct answer |
| **Next**      | Skip to the next quote |
| **Exit**      | End the current game session |

---

### Built with:

- **Python** 
- **aiogram 3** 
- **asyncio** 
- **json** 
- **dotenv** 
- **os** 
---

