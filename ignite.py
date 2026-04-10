"""
           ───── ୨୧ ─────
                   TeamDev
"""

import sys
import logging
import telebot
import threading
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from config import BOT_TOKEN
from TeamDev.core.database import init_db
from TeamDev.handlers import (
    register_start_handlers,
    register_download_handlers,
    register_admin_handlers,
)

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("TeamDev")

# ---------------- HEALTH SERVER (IMPORTANT) ----------------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    log.info(f"[TeamDev] => Health server running on port {port}")
    server.serve_forever()

# ---------------- MAIN BOT ----------------
def main():
    if not BOT_TOKEN:
        log.error("[TeamDev] => BOT_TOKEN not set — aborting.")
        sys.exit(1)

    # 👉 Start health server (Railway fix)
    threading.Thread(target=run_server, daemon=True).start()

    log.info("[TeamDev] => Connecting to MongoDB and creating indexes...")
    init_db()

    log.info("[TeamDev] => Starting bot...")
    bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

    register_start_handlers(bot)
    register_download_handlers(bot)
    register_admin_handlers(bot)

    info = bot.get_me()
    log.info(f"[TeamDev] => Bot live | @{info.username} | id={info.id}")

    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=20,
        logger_level=logging.WARNING,
    )

if __name__ == "__main__":
    main()
