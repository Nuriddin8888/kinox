import math

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import get_all_movie, get_all_users
from generate_code import get_movie_name

CHANNEL_ID = -1004419651547


async def check_subscription(user_id, bot: Bot):
    member = await bot.get_chat_member(CHANNEL_ID, user_id)
    return member.status in [
        "member",
        "administrator",
        "creator"
    ]



def subscription_button():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url="https://t.me/uzbkinoxuz")
            ],
            [
                InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")
            ]
        ]
    )

    return keyboard




def movie_pagination(page=1):
    movies = get_all_movie()
    per_page = 6

    total_pages = math.ceil(len(movies) / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    current_movies = movies[start:end]

    text = "🎬 Filmlar ro'yxati:\n\n"

    for movie in current_movies:
        movie_code = movie[4]
        description = movie[2]
        movie_time = movie[5]

        movie_name = get_movie_name(description)

        text += (
            f"🎥 {movie_name}\n"
            f"🆔 Kod: {movie_code}\n"
            f"⌚️ Qo'shilgan vaqt: {movie_time}\n\n"
        )

    keyboard = []

    buttons = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"movie_page:{page-1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data="ignore"
        )
    )

    if page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"movie_page:{page+1}"
            )
        )

    keyboard.append(buttons)

    return text, InlineKeyboardMarkup(inline_keyboard=keyboard)


def users_pagination(page=1):
    users = get_all_users()
    per_page = 6

    total_pages = math.ceil(len(users) / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    current_users = users[start:end]

    text = "👥 Userlar ro'yxati:\n\n"

    for user in current_users:
        user_id = user[0]
        full_name = user[1]
        username = user[2]
        created_at = user[3]

        text += (
            f"🆔 User Id: {user_id}\n"
            f"👤 Full Name: {full_name}\n"
            f"🫆 Username: @{username}\n"
            f"⌚️ Created at: {created_at}\n\n"
        )

    keyboard = []

    buttons = []

    if page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"user_page:{page-1}"
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data="ignore"
        )
    )

    if page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"user_page:{page+1}"
            )
        )

    keyboard.append(buttons)

    return text, InlineKeyboardMarkup(inline_keyboard=keyboard)


confirm_reklama_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data="confirm_reklama"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="cancel_reklama"
            )
        ]
    ]
)


admin_panel_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Film qo'shish", callback_data="add_film"),
            InlineKeyboardButton(text="Film ko'rish", callback_data="show_film")
        ],
        [
            InlineKeyboardButton(text="Reklama qo'shish", callback_data="add_reklama")
        ],
        [
            InlineKeyboardButton(text="Userlarni ko'rish", callback_data="show_users"),
            InlineKeyboardButton(text="Film o'chirish", callback_data="delete_movie")
        ]
    ]
)