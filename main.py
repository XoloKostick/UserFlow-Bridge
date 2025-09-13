from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path
from app.db.base import select_db
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from app.core.config import API
from app.db.base import init_db, insert_db
from app.core.logger import logger

app = FastAPI(title='UserFlow Bridge', version='1.0')
API_TOKEN = API
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    user = message.from_user
    text = f"""
<b>🎉 Добро пожаловать в UserFlow Bridge!</b>

📊 <b>Твои данные:</b>
├ ID: <code>{user.id}</code>
├ Имя: <i>{user.first_name or 'не указано'}</i>
├ Username: @{user.username or 'не указан'}
└ Статус: <b>✅ активирован</b>
    """
    insert_db(username=user.username, id=user.id)
    await message.answer(text=text, parse_mode='HTML')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    users = select_db()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "users": users
        }
    )

@app.get("/api/users")
async def get_users_api():
    users = select_db()
    return users

async def run_bot():
    logger.info("Бот запускается...")
    await dp.start_polling(bot)

async def run_fastapi():
    import uvicorn
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    logger.info("FastAPI запускается...")
    await server.serve()

async def main():
    await asyncio.gather(
        run_fastapi(),
        run_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())