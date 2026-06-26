from aiogram.fsm.state import State, StatesGroup


class FilmState(StatesGroup):
    film_video = State()
    film_desc = State()


class DeleteMovie(StatesGroup):
    code = State()


class ReklamaState(StatesGroup):
    poster = State()
    content = State()