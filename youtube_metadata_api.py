from flask import Flask, request, jsonify
import boto3
import feedparser
import re

app = Flask(__name__)
# Connect to local DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # or 'http://host.docker.internal:8000' on Windows
    aws_access_key_id="dummy",  # Use dummy credentials for local DynamoDB
    aws_secret_access_key="dummy",
    region_name="us-east-1"  # Specify a valid AWS region
)
table_name = 'YouTubeVideos'
table = dynamodb.Table(table_name)

def get_youtube_rss_feed(channel_id):
    """Fetch video metadata from YouTube's public RSS feed."""
    rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
    feed = feedparser.parse(rss_url)
    
    if 'entries' not in feed:
        return None  # Invalid channel or no data available
    
    videos = []
    for entry in feed.entries[:5]:  # Limit to recent 5 videos
        videos.append({
            'video_id': entry.id,
            'title': entry.title,
            'published': entry.published,
            'link': entry.link
        })
    return videos

def fetch_from_dynamodb(channel_id):
    """Retrieve video metadata from DynamoDB."""
    try:
        response = table.get_item(Key={'channel_id': channel_id})
        return response.get('Item', {}).get('videos')
    except Exception as e:
        print(f"Error fetching from DynamoDB: {e}")
        return None

def store_in_dynamodb(channel_id, videos):
    """Store video metadata in DynamoDB (limit to 5 recent videos)."""
    videos = videos[:5]  # Limit to 5 videos
    table.put_item(Item={'channel_id': channel_id, 'videos': videos})

def is_valid_channel_id(channel_id):
    return bool(re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id))

@app.route('/videos', methods=['GET'])
def get_videos():
    channel_id = request.args.get('channel_id')
    if not channel_id:
        return jsonify({'error': 'Missing channel_id'}), 400
    if not is_valid_channel_id(channel_id):
        return jsonify({'error': 'Invalid channel_id format'}), 400
    
    # Check in DynamoDB first
    videos = fetch_from_dynamodb(channel_id)
    if videos:
        print("Metadata retrieved from DynamoDB")
        return jsonify({'source': 'dynamodb', 'videos': videos})
    
    # Fetch from third-party source if not found
    videos = get_youtube_rss_feed(channel_id)
    if videos:
        store_in_dynamodb(channel_id, videos)
        print("Metadata retrieved from rss feed")
        return jsonify({'source': 'rss_feed', 'videos': videos})
    
    return jsonify({'error': 'Invalid channel_id'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
