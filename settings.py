from dotenv import load_dotenv

import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
JWT_SECRET_KEY = "UOtCmhFOxRX0Im3o74PUikcYPHjhndtGsacIyOZnsHNjRWU7I1ouiDlDxCK5XXCu"
