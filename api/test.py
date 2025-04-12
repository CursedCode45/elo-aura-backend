import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


def save_binary_image_to_bucket(binary_image, bucket_path):
    supabase = create_client(url, key)
    response = supabase.storage.from_("user-images").upload(
        file=binary_image,
        path=bucket_path,
    )
    print(response)



