import re

from app.config_loader import load_languages_config

EXTENSION_TO_LANGUAGE = load_languages_config()


def detect_language_from_title(title):
    title = title.lower()

    match = re.search(r"([\w\-.]+\.[a-zA-Z0-9]+)", title)

    if not match:
        return None

    filename = match.group(1)

    for extension, language in EXTENSION_TO_LANGUAGE.items():
        if filename.endswith(extension):
            return language

    return None