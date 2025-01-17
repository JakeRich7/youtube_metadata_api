import boto3

# Connect to local DynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # or 'http://host.docker.internal:8000' on Windows
    aws_access_key_id="dummy",  # Use dummy credentials for local DynamoDB
    aws_secret_access_key="dummy",
    region_name="us-east-1"  # Specify a valid AWS region
)
table = dynamodb.create_table(
    TableName='YouTubeVideos',
    KeySchema=[{'AttributeName': 'channel_id', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'channel_id', 'AttributeType': 'S'}],
    ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
)
table.wait_until_exists()
print("Table created!")