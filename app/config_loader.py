import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"


def load_json_config(filename):
    path = CONFIG_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_apps_config():
    return load_json_config("apps.json")


def load_languages_config():
    return load_json_config("languages.json")