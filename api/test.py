import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


with open("../user_images/1/16.jpg", "rb") as f:
    response = supabase.storage.from_("user-images").upload(
        file=f,
        path="1/16.jpg",
    )


print(response)


