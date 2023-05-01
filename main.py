import os
from config import config

from utils import get_youtube_data, create_database, save_data_to_database


def main():
    api_key = os.getenv('YT-API-KEY')
    channel_ids = [
        "@ColbertLateShow",
        "@JimmyKimmelLive",
        "@fallontonight",
        "@LateNightSeth",
        "@TheLateLateShow"
    ]

    params = config()
    data = get_youtube_data(api_key, channel_ids)

    create_database('YouTube_DB', params)
    save_data_to_database(data, 'YouTube_DB', params)


if __name__ == '__main__':
    main()
