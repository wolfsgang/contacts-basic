from src.base import create_app
from config import app_config

flask_app = create_app(app_config)
# print flask_app.url_map
#flask_app.run()
