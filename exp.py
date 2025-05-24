import dotenv
import os
dotenv.load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
dotenv.load_dotenv(".env")
key = os.getenv("GOOGLE_API_KEY")
print(key)

