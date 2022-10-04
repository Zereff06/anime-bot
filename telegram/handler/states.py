from aiogram.dispatcher.filters.state import StatesGroup, State


# class FindMedia(StatesGroup):
# media_type = State()
# site = State()
# name = State()
# set_media_state = State()

class Questions(StatesGroup):
    how_many_series_user_watch = State()
