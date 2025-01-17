# YouTube Metadata API

This REST API retrieves recent video metadata from a YouTube channel. The data is fetched from DynamoDB if available, or from YouTube's RSS feed if not. The API stores fetched metadata in DynamoDB for future use.

## Features
- Fetches video metadata from DynamoDB or YouTube RSS feed
- Stores new video metadata in local DynamoDB
- Returns details such as video ID, title, published date, and link

## Requirements
- Python 3.x
- Flask (`pip install flask`)
- Boto3 (`pip install boto3`)
- Feedparser (`pip install feedparser`)
- DynamoDB Local or AWS DynamoDB.

## Setup

1. Install dependencies:
- `pip install flask boto3 feedparser`

2. Run DynamoDB locally
- `docker run -p 8000:8000 amazon/dynamodb-local`

3. Create dynamoDB 'YouTubeVideos' Table:
- `python dynamodb_create_table.py`

4. Start the API:
- `python app.py`
- The API will run on port 5000

## API Endpoints

### `GET /videos`
- Fetches recent video metadata for a given YouTube channel.

#### Query Parameters:
- `channel_id` (required): YouTube channel ID

#### Example Request:
- GET http://localhost:5000/videos?channel_id=UCX6OQ3DkcsbYNE6H8uQQuVA

#### Example Response:
```json
{
    "source": "rss_feed",
    "videos": [
        {
            "video_id": "dQw4w9WgXcQ",
            "title": "Never Gonna Give You Up",
            "published": "2021-10-01T00:00:00Z",
            "link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    ]
}
```

## Troubleshooting
Run the following python files as needed:
- Create table: `python dynamodb_create_table.py`
- Scan and print table: `python dynamodb_scan_table.py`
- Delete table: `python dynamodb_delete_table.py`

## Code Overview
- The API checks DynamoDB for video metadata
- If not found, it fetches data from YouTube’s RSS feed and stores it in DynamoDB
- Flask handles the API, Boto3 interacts with DynamoDB, and Feedparser parses the RSS feed