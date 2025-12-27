from cnl import create_app
from cnl.extensions import db
import os

app = create_app()

# Run this block ONLY in development
if os.getenv("FLASK_ENV") == "development":
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(host="0.0.0.0", port=5000, debug=debug)
