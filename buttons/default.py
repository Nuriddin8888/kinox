from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_number_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Joylashuv 📍", request_location=True)
        ]
    ], resize_keyboard=True
)
