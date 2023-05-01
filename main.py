import os
from config import config
import google.auth
from googleapiclient.discovery import build


from utils import get_youtube_data, create_database, save_data_to_database


def main():
    api_key = os.getenv('YT-API-KEY')

    channel_ids = [
        "UCMtFAi84ehTSYSE9XoHefig",  # "@ColbertLateShow",
        # "UCa6vGFO9ty8v5KZJXQxdhaw",  # "@JimmyKimmelLive",
        # "UC8-Th83bH_thdKZDJCrn88g",  # "@fallontonight",
        # "UCVTyTA7-g9nopHeHbeuvpRA",  # "@LateNightSeth",
        # "UCJ0uqCI0Vqr2Rrt1HseGirg",  # "@TheLateLateShow"
    ]

    data = get_youtube_data(api_key, channel_ids)
    params = config()
    # create_database('YouTube_DB', params)
    # save_data_to_database(data, 'YouTube_DB', params)

if __name__ == '__main__':
    main()
