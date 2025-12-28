from aiogram import types, F
from app.storage import channels, files, users

def register_user(dp, bot):

    @dp.message(F.text == "/start")
    async def start(message: types.Message):
        users.add(message.from_user.id)

        if not channels or not files:
            await message.answer("Бот ещё не настроен администратором")
            return

        for channel in channels:
            try:
                member = await bot.get_chat_member(channel, message.from_user.id)
                if member.status in ["left", "kicked"]:
                    await message.answer(
                        "❗ Подпишись на все каналы и напиши /start ещё раз"
                    )
                    return
            except:
                await message.answer("Ошибка проверки подписки")
                return

        await message.answer_document(files[0])
