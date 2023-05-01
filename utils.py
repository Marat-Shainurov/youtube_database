from typing import Any
from googleapiclient.discovery import build


def get_youtube_data(api_key: str, channel_ids: list[str]) -> list[dict[str, Any]]:
    """Gets data about YouTube channels via API YouTube."""
    youtube = build('youtube', 'v3', developerKey=api_key)

    data = []
    videos_data = []
    next_page_token = None
    for channel_id in channel_ids:
        channel_data = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()

        while True:
            response = youtube.search().list(part='id,snippet', channelId=channel_id, type='video',
                                             order='date', maxResults=50, pageToken=next_page_token).execute()
            videos_data.extend(response['items'])
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        data.append({
            'channel': channel_data['items'][0],
            'videos': videos_data
        })
        return data

def create_database(name: str, params: dict) -> None:
    """Creates database and tables"""


def save_data_to_database(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Saves data to the database"""
