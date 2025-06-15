import dotenv
import os

dotenv.load_dotenv()

from my_web import app

app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"))
