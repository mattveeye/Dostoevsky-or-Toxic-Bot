import os
import json
import random
from aiogram.client.default import DefaultBotProperties

import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") #change it on yours
DOSTOEVSKY_FILE = "dostoevsky.json"
TOXIC_FILE = "toxic.json"

START_PHOTO = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%2Fid%2FOIP.ccT7BevgRWSahvmUH19kTQHaI5%3Fpid%3DApi&f=1&ipt=dcdf3bbfaae2486d1c33556a0614b4769f653bd4cd2e82dac7e105fc8b0c8cec&ipo=images"

# buttons
BTN_START = "Start Game"
BTN_DOST = "Dostoevsky"
BTN_TOX = "Toxic Guy"
BTN_GIVEUP = "Give Up"
BTN_EXIT = "Exit"
BTN_NEXT = "Next"

# quotes fetching
def load_quotes(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [str(q).strip() for q in data if str(q).strip()]
            else:
                return []
    except:
        print(f"reading error {filename}")
        return []

dost_quotes = load_quotes(DOSTOEVSKY_FILE)
toxic_quotes = load_quotes(TOXIC_FILE)


quotes_pool = []
for q in dost_quotes:
    quotes_pool.append((q, "dost"))
for q in toxic_quotes:
    quotes_pool.append((q, "toxic"))

if not quotes_pool:
    print("NO QUOTES FOUND CHECK YOUR JSON FILES")


user_states = {}

#keyboards
def get_main_kb():
    kb = [[KeyboardButton(text=BTN_START)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Нажми кнопку, чтобы начать")

def get_answer_kb():
    kb = [
        [KeyboardButton(text=BTN_DOST), KeyboardButton(text=BTN_TOX)],
        [KeyboardButton(text=BTN_GIVEUP), KeyboardButton(text=BTN_EXIT)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выбери вариант")

def get_next_kb():
    kb = [[KeyboardButton(text=BTN_NEXT)], [KeyboardButton(text=BTN_EXIT)]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Продолжим?")

#game logic
def start_game(user_id):
    deck = quotes_pool.copy()
    random.shuffle(deck)
    user_states[user_id] = {
        "deck": deck,
        "current": None,
        "score": 0,
        "total": 0
    }

def get_next_quote(user_id):
    if user_id not in user_states:
        start_game(user_id)
    state = user_states[user_id]
    if not state["deck"]:
        # mix again if 0
        state["deck"] = quotes_pool.copy()
        random.shuffle(state["deck"])
    quote, author = state["deck"].pop()
    state["current"] = (quote, author)
    return quote, author

# bot itself
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""

    # start
    if text == "/start":
        caption = (
            "Hello! This is a game: guess who said the quote — *Dostoevsky* or *a toxic guy from Twitter*?\n\n"
            "Rules are simple: you'll see a quote, choose one of two options. Good luck!"
        )
        try:
            await message.answer_photo(photo=START_PHOTO, caption=caption, reply_markup=get_main_kb())
        except:
            await message.answer(caption, reply_markup=get_main_kb())
        return

    #  /stats
    if text == "/stats":
        if user_id not in user_states:
            await message.answer("You have not played yet. Press Start Game.", reply_markup=get_main_kb())
        else:
            s = user_states[user_id]
            await message.answer(f"Your score: {s['score']}/{s['total']}")
        return

    #  Start Game
    if text == BTN_START:
        start_game(user_id)
        quote, label = get_next_quote(user_id)
        user_states[user_id]["current"] = (quote, label)
        await message.answer(f"Who said it?\n\n*{quote}*", reply_markup=get_answer_kb())
        return

    # if one is not in game
    if user_id not in user_states:
        await message.answer("Type Start Game or  /start", reply_markup=get_main_kb())
        return

    state = user_states[user_id]
    current = state["current"]

    # if theres no current quote give it
    if not current:
        quote, label = get_next_quote(user_id)
        state["current"] = (quote, label)
        await message.answer(f"Who said it? \n\n*{quote}*", reply_markup=get_answer_kb())
        return

    quote_text, correct = current

    # exit
    if text == BTN_EXIT:
        score = state["score"]
        total = state["total"]
        await message.answer(f"Game's over. Your result: {score}/{total}", reply_markup=ReplyKeyboardRemove())
        del user_states[user_id]
        return

    # giveup
    if text == BTN_GIVEUP:
        state["total"] += 1
        answer = "Dostoevsky" if correct == "dost" else "Toxic Guy"
        await message.answer(f"Correct answer: *{answer}*\n", reply_markup=get_next_kb())
        state["current"] = None
        return

    # answer
    if text == BTN_DOST or text == BTN_TOX:
        guess = "dost" if text == BTN_DOST else "toxic"
        state["total"] += 1
        if guess == correct:
            state["score"] += 1
            await message.answer("Correct! 🎉", reply_markup=get_next_kb())
        else:
            answer = "Dostoevsky" if correct == "dost" else "Toxic Guy"
            await message.answer(f"Wrong. Right answer: *{answer}*", reply_markup=get_next_kb())
        state["current"] = None
        return

    # next quote
    if text == BTN_NEXT:
        quote, label = get_next_quote(user_id)
        state["current"] = (quote, label)
        await message.answer(f"Who said that?\n\n*{quote}*", reply_markup=get_answer_kb())
        return

    # unknown command
    await message.answer("didn't get. use button", reply_markup=get_answer_kb())

# bot running
async def main():
    if not BOT_TOKEN:
        print("YOU FORGOT ABOUT BOT_TOKEN. CREATE .ENV")
        return
    print("bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())