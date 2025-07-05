from app import create_app
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)