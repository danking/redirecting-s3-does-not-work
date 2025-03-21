import boto3
import boto3.session

# Create a new session (optionally specify region_name if your endpoint requires it)
session = boto3.session.Session(profile_name='PowerUserAccess-375504701696')

# Create an S3 client using a custom endpoint
s3 = session.client(
    service_name='s3',
    endpoint_url='http://localhost:5001/',
)

# List buckets
response = s3.list_buckets()
for bucket in response.get('Buckets', []):
    print(bucket['Name'])
