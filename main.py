import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database import init_db, add_user, get_user, add_movie, get_movie, delete_movie, get_all_users
from buttons.inline import check_subscription, subscription_button, admin_panel_button, movie_pagination, users_pagination, confirm_reklama_btn
from state import FilmState, DeleteMovie, ReklamaState
from generate_code import generate_movie_code

from config import TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)


bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if not await check_subscription(user_id, bot):
        await message.answer(
            "Botdan foydalanish uchun kanalga obuna bo'ling!",
            reply_markup=subscription_button()
        )
        return

    if not get_user(user_id):
        add_user(
            user_id,
            message.from_user.full_name,
            message.from_user.username
        )

    await message.answer("Salom Botimizga xush kelibsiz\nFilm kodini yuboring")


@dp.callback_query(F.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):

    if not await check_subscription(callback.from_user.id, bot):
        await callback.answer(
            "Siz hali kanalga obuna bo'lmagansiz!",
            show_alert=True
        )
        return

    if not get_user(callback.from_user.id):
        add_user(
            callback.from_user.id,
            callback.from_user.full_name,
            callback.from_user.username
        )

    await callback.message.edit_text(
        "✅ Obuna tasdiqlandi!\n"
        "Botimizga xush kelibsiz.\n"
        "Film kodini yuboring."
    )


@dp.message(Command("admin"))
async def admin_panel_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        await message.answer("Salom Admin botga xush kelibsiz", reply_markup=admin_panel_button)
    else:
        pass


@dp.callback_query(F.data == "add_film")
async def add_film_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Film videosini yuboring")
    await state.set_state(FilmState.film_video)


@dp.message(F.video, FilmState.film_video)
async def get_film_video(message: types.Message, state: FSMContext):
    video = message.video.file_id
    await state.update_data(film_video=video)
    await message.answer("Film videosi qabul qilindi")
    await message.answer("Film tavsifini yuboring")
    await state.set_state(FilmState.film_desc)



@dp.message(F.text, FilmState.film_desc)
async def get_film_desc(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data(film_desc=desc)

    data = await state.get_data()

    video = data.get("film_video")
    desc = data.get("film_desc")

    code = generate_movie_code()

    add_movie(video, desc, code)

    caption = f"""
🎬 Film muvaffaqiyatli qo'shildi.

🆔 Film kodi: <code>{code}</code>
        """

    await message.answer_video(video=video, caption=caption, parse_mode="HTML")
    await state.clear()



@dp.callback_query(F.data == "show_film")
async def show_movies(callback: types.CallbackQuery):

    text, markup = movie_pagination(page=1)

    await callback.message.edit_text(
        text,
        reply_markup=markup
    )
    

@dp.callback_query(F.data.startswith("movie_page:"))
async def movie_pages(callback: types.CallbackQuery):

    page = int(callback.data.split(":")[1])

    text, markup = movie_pagination(page)

    await callback.message.edit_text(
        text,
        reply_markup=markup
    )


@dp.callback_query(F.data == "show_users")
async def show_users(callback: types.CallbackQuery):

    text, markup = users_pagination(page=1)

    await callback.message.edit_text(
        text,
        reply_markup=markup
    )


@dp.callback_query(F.data.startswith("user_page:"))
async def user_pages(callback: types.CallbackQuery):

    page = int(callback.data.split(":")[1])

    text, markup = users_pagination(page)

    await callback.message.edit_text(
        text,
        reply_markup=markup
    )


@dp.callback_query(F.data == "delete_movie")
async def delete_movie_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("O'chirmoqchi bo'lgan film kodini yozing")
    await state.set_state(DeleteMovie.code)


@dp.message(DeleteMovie.code)
async def delete_code(message: types.Message, state: FSMContext):
    movie_code = message.text
    movie = get_movie(movie_code)
    if movie:
        delete_movie(movie_code)
        await message.answer("Film o'chirildi.")
        await state.clear()
    else:
        await message.answer("Film mavjud emas")
        await state.clear()


@dp.callback_query(F.data == "add_reklama")
async def add_reklama_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Reklama posterini yuboring")
    await state.set_state(ReklamaState.poster)


@dp.message(ReklamaState.poster, F.photo)
async def get_reklama_photo(
    message: types.Message,
    state: FSMContext
):
    photo_id = message.photo[-1].file_id
    caption = message.caption or ""

    await state.update_data(
        media_type="photo",
        file_id=photo_id,
        caption=caption
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_id,
        caption=caption,
        reply_markup=confirm_reklama_btn
    )


@dp.message(ReklamaState.poster, F.video)
async def get_reklama_video(
    message: types.Message,
    state: FSMContext
):
    video_id = message.video.file_id
    caption = message.caption or ""

    await state.update_data(
        media_type="video",
        file_id=video_id,
        caption=caption
    )

    await bot.send_video(
        chat_id=ADMIN_ID,
        video=video_id,
        caption=caption,
        reply_markup=confirm_reklama_btn
    )


@dp.callback_query(F.data == "confirm_reklama")
async def confirm_reklama(
    callback: types.CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()

    media_type = data.get("media_type")
    file_id = data.get("file_id")
    caption = data.get("caption")

    users = get_all_users()

    success = 0

    for user in users:
        try:
            user_id = user[0]  # user_id ustuni

            if media_type == "photo":
                await bot.send_photo(
                    chat_id=user_id,
                    photo=file_id,
                    caption=caption
                )

            elif media_type == "video":
                await bot.send_video(
                    chat_id=user_id,
                    video=file_id,
                    caption=caption
                )

            success += 1

        except Exception:
            pass

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.message.answer(
        f"✅ Reklama {success} ta foydalanuvchiga yuborildi."
    )

    await state.clear()


@dp.callback_query(F.data == "cancel_reklama")
async def cancel_reklama(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await state.clear()

    await callback.message.edit_reply_markup(
        reply_markup=None
    )

    await callback.message.answer(
        "❌ Reklama bekor qilindi."
    )


@dp.message(F.text)
async def get_movie_code(message: types.Message):
    code = message.text
    movie = get_movie(code)
    if not movie:
        await message.answer("Bunday film kodi mavjud emas ❌")
    else:
        await message.answer_video(video=movie[0][1], caption=movie[0][2])


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())


