import os
import boto3
from botocore.exceptions import NoCredentialsError
from PIL import Image
from simple_image_download import simple_image_download as simp
from modules.label_image import text_recognition
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

# Initialize AWS S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def fetch_images(keyword, limit=100):
    downloader = simp.Downloader()
    downloader.directory = 'dataset/'
    cache = downloader.search_urls(keyword, limit=limit)
    downloader.download(download_cache=True)
    image_paths = [os.path.join(f'dataset/{keyword}', filename) for filename in os.listdir(f'dataset/{keyword}') if filename.endswith(('.png', '.jpg', '.jpeg'))]
    return image_paths, downloader.get_urls()

def upload_to_s3(file_name, bucket):
    object_name = os.path.basename(os.path.dirname(file_name))
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f'Successfully uploaded {file_name} to {bucket}/{object_name}')
    except NoCredentialsError:
        print("Credentials not available")

def process_and_upload_images(image_paths, image_urls):
    metadata = []
    for image_path, image_url in zip(image_paths, image_urls):
        image_id = os.path.basename(image_path)
        try:
            img = Image.open(image_path)
            # Optionally, you can process the image here if needed
            img.verify()  # Verify that it's an image
            upload_to_s3(image_path, AWS_S3_BUCKET_NAME)
            metadata.append({
                'image': f'{image_id}',
                'description': text_recognition(image_url),
                'url': image_url
            })
        except Exception as e:
            print(f"Failed to process image {image_id}: {e}")
    return metadata

def save_metadata(metadata, save_dir):
    import json
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with open(os.path.join(save_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f)

# Example usage
keyword = 'bibleversecalligraphy'
image_paths, image_urls = fetch_images(keyword, limit=10)
metadata = process_and_upload_images(image_paths, image_urls)
save_metadata(metadata, save_dir=f'dataset/{keyword}')
