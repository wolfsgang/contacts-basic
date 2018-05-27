from src.base import create_app
from config import app_config

if __name__ == "__main__":
    flask_app = create_app(app_config)
    print flask_app.url_map
    flask_app.run(host="127.0.0.1", port=5000)
