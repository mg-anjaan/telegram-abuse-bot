from bot import app
from aiohttp import web

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=10000)