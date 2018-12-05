import os

from app import create_app

# os.getenv('APP_SETTINGS')

app = create_app("development")

if __name__ == '__main__':
    app.run(debug=True)
