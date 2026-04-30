import time
from datetime import datetime

import psutil
import win32gui
import win32process

from app.database import (
    init_db,
    add_bulk_seconds_to_daily_stats,
    add_bulk_seconds_to_daily_language_stats
)

from app.classifier import classify_app
from app.language_detector import detect_language_from_title

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()

        if not hwnd:
            return None

        title = win32gui.GetWindowText(hwnd)

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        if not pid or pid <= 0:
            return None

        process = psutil.Process(pid).name()

        return {
            "title": title,
            "process": process
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, ValueError):
        return None


def main():
    init_db()

    print("Coding Stats tracker started...")
    
    pending_language_stats = {}
    pending_stats = {}
    last_active = None
    last_flush = time.time()

    FLUSH_INTERVAL = 15

    try:
        while True:
            active = get_active_window()
            
            
            language = detect_language_from_title(active["title"])
            if language:
                pending_language_stats[language] = pending_language_stats.get(language, 0) + 1
    
    

            if active:
                category = classify_app(active["process"], active["title"])

                if category:
                    key = (active["process"], category)
                    pending_stats[key] = pending_stats.get(key, 0) + 1

                    if active != last_active:
                        print(f"Tracking: {active['process']} | {category}")
                        last_active = active

            if time.time() - last_flush >= FLUSH_INTERVAL:
                add_bulk_seconds_to_daily_stats(pending_stats)
                add_bulk_seconds_to_daily_language_stats(pending_language_stats)

                pending_stats.clear()
                pending_language_stats.clear()
                last_flush = time.time()

            time.sleep(1)

    except KeyboardInterrupt:
        add_bulk_seconds_to_daily_stats(pending_stats)
        add_bulk_seconds_to_daily_language_stats(pending_language_stats)
        print("Tracker stopped.")

if __name__ == "__main__":
    main()