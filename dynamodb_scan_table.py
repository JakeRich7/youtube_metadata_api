import boto3
import json

# Connect to local DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
    region_name="us-east-1"
)

table = dynamodb.Table("YouTubeVideos")

def scan_table():
    response = table.scan()
    items = response.get("Items", [])
    
    print("🔹 DynamoDB Table Contents:")
    print(json.dumps(items, indent=4))

if __name__ == "__main__":
    scan_table()