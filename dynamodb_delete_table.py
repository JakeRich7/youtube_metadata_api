import boto3

# Connect to local DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
    region_name="us-east-1"
)

table = dynamodb.Table("YouTubeVideos")

def delete_table():
    try:
        # Delete the table entirely
        table.delete()
        print("🔹 DynamoDB Table Deleted Successfully")
    except Exception as e:
        print(f"Error deleting the table: {e}")

if __name__ == "__main__":
    delete_table()
