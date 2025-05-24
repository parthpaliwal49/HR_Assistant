import dotenv
import os

dotenv.load_dotenv(".env")
key = os.getenv("GOOGLE_API_KEY")
print(key)

