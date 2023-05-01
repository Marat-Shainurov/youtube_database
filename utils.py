from typing import Any
from googleapiclient.discovery import build
import psycopg2


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


def create_database(db_name: str, params: dict) -> None:
    """Creates database and tables"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE channels
            (
            channel_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            views INTEGER,
            subscribers INTEGER,
            videos INTEGER,
            channel_url TEXT
            )
            """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE videos 
            (
            video_id SERIAL PRIMARY KEY,
            channel_id INT REFERENCES channels(channel_id),
            title VARCHAR NOT NULL,
            publish_date DATE,
            video_url TEXT
            )
            """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], db_name: str, params: dict) -> None:
    """Saves data to the database"""
