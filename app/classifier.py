from app.config_loader import load_apps_config

APPS_CONFIG = load_apps_config()


def classify_app(process, title):
    app_config = APPS_CONFIG.get(process)

    if not app_config:
        return None

    category = app_config.get("category")

    if process.lower() in ["chrome.exe", "msedge.exe", "firefox.exe"]:
        title = title.lower()

        if "youtube" in title or "instagram" in title or "tiktok" in title:
            return "Distraction"

        if "localhost" in title or "github" in title or "docs" or "stackoverflow" in title:
            return "Dev Browser"

    return category


def get_process_display_name(process):
    app_config = APPS_CONFIG.get(process)

    if not app_config:
        return process

    return app_config.get("display_name", process)