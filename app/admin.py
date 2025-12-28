from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode

from app.config import ADMINS
from app.storage import channels, files, users
from app.states import AddFileState

def register_admin(dp):

    @dp.message(F.text.startswith("/addchannel"))
    async def add_channel(message: types.Message):
        if message.from_user.id not in ADMINS:
            return
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("Используй: /addchannel channel_username")
            return
        channel = args[1].replace("@", "")
        if channel not in channels:
            channels.append(channel)
            await message.answer(f"✅ Канал {channel} добавлен")

    @dp.message(F.text == "/addfile")
    async def add_file_start(message: types.Message, state: FSMContext):
        if message.from_user.id not in ADMINS:
            return
        await message.answer("📎 Отправь файл следующим сообщением")
        await state.set_state(AddFileState.waiting_file)

    @dp.message(AddFileState.waiting_file, F.document)
    async def add_file(message: types.Message, state: FSMContext):
        file_id = message.document.file_id
        files.append(file_id)
        await message.answer("✅ Файл добавлен")
        await state.clear()

    @dp.message(F.text == "/admin")
    async def admin_panel(message: types.Message):
        if message.from_user.id not in ADMINS:
            return
        text = (
            "⚙️ Админ-панель\n\n"
            f"📢 Каналов: {len(channels)}\n"
            f"📁 Файлов: {len(files)}\n"
            f"👤 Пользователей: {len(users)}\n\n"
            "/addchannel — добавить канал\n"
            "/addfile — добавить файл\n"
        )
        await message.answer(text, parse_mode=ParseMode.HTML)
