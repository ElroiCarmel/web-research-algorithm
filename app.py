import os
from my_web import app

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("FLASK_RUN_PORT"), host="0.0.0.0")
