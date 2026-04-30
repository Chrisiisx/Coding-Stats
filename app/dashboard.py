import sqlite3
from datetime import date

import customtkinter as ctk
from app.database import init_db
from app.classifier import get_process_display_name

DB_NAME = "codingstats.db"

PROCESS_DISPLAY_NAMES = {
    "Code.exe": "Visual Studio Code",
    "WindowsTerminal.exe": "Terminal",
    "Postman.exe": "Postman",
    "Discord.exe": "Discord",
}

def get_display_name(process):
    return PROCESS_DISPLAY_NAMES.get(process, process)

def format_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m"

    if minutes > 0:
        return f"{minutes}m {secs}s"

    return f"{secs}s"


def get_today_category_stats():
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(total_seconds)
        FROM daily_app_stats
        WHERE date = ?
        GROUP BY category
        ORDER BY SUM(total_seconds) DESC
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_today_software_stats():
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT process, SUM(total_seconds)
        FROM daily_app_stats
        WHERE date = ?
        GROUP BY process
        ORDER BY SUM(total_seconds) DESC
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_today_language_stats():
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT language, total_seconds
        FROM daily_language_stats
        WHERE date = ?
        ORDER BY total_seconds DESC
    """, (today,))

    rows = cursor.fetchall()
    conn.close()

    return rows


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Coding Stats")
        self.geometry("620x520")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title_label = ctk.CTkLabel(
            self,
            text="Coding Stats",
            font=("Segoe UI", 30, "bold")
        )
        self.title_label.pack(pady=(24, 4))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Today's development activity",
            font=("Segoe UI", 14)
        )
        self.subtitle_label.pack(pady=(0, 18))

        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(pady=(0, 16))

        self.overview_button = ctk.CTkButton(
            self.nav_frame,
            text="Overview",
            width=120,
            command=self.render_overview
        )
        self.overview_button.pack(side="left", padx=6)

        self.software_button = ctk.CTkButton(
            self.nav_frame,
            text="Software",
            width=120,
            command=self.render_software
        )
        self.software_button.pack(side="left", padx=6)

        self.languages_button = ctk.CTkButton(
            self.nav_frame,
            text="Languages",
            width=120,
            command=self.render_languages
        )
        self.languages_button.pack(side="left", padx=6)

        self.total_label = ctk.CTkLabel(
            self,
            text="Total: 0s",
            font=("Segoe UI", 20, "bold")
        )
        self.total_label.pack(pady=(0, 18))

        self.stats_frame = ctk.CTkFrame(self, corner_radius=16)
        self.stats_frame.pack(fill="both", expand=True, padx=24, pady=(0, 18))

        self.refresh_button = ctk.CTkButton(
            self,
            text="Refresh",
            width=160,
            command=self.render_current_page
        )
        self.refresh_button.pack(pady=(0, 20))

        self.current_page = "overview"
        self.render_overview()

    def clear_stats_frame(self):
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

    def render_current_page(self):
        if self.current_page == "overview":
            self.render_overview()
        elif self.current_page == "software":
            self.render_software()
        elif self.current_page == "languages":
            self.render_languages()

    def render_overview(self):
        self.current_page = "overview"
        self.clear_stats_frame()

        stats = get_today_category_stats()

        if not stats:
            self.render_empty("Nessun dato registrato oggi.")
            self.total_label.configure(text="Total: 0s")
            return

        total = sum(seconds for _, seconds in stats)
        self.total_label.configure(text=f"Total: {format_seconds(total)}")

        for category, seconds in stats:
            self.render_row(category, seconds)

    def render_software(self):
        self.current_page = "software"
        self.clear_stats_frame()

        stats = get_today_software_stats()

        if not stats:
            self.render_empty("Nessun software registrato oggi.")
            self.total_label.configure(text="Software: 0s")
            return

        total = sum(seconds for _, seconds in stats)
        self.total_label.configure(text=f"Software: {format_seconds(total)}")

        for process, seconds in stats:
            self.render_row(get_process_display_name(process), seconds)

    def render_languages(self):
        self.current_page = "languages"
        self.clear_stats_frame()

        stats = get_today_language_stats()

        if not stats:
            self.render_empty("Nessun linguaggio rilevato oggi.")
            self.total_label.configure(text="Languages: 0s")
            return

        total = sum(seconds for _, seconds in stats)
        self.total_label.configure(text=f"Languages: {format_seconds(total)}")

        for language, seconds in stats:
            self.render_row(language, seconds)

    def render_empty(self, message):
        ctk.CTkLabel(
            self.stats_frame,
            text=message,
            font=("Segoe UI", 15)
        ).pack(pady=40)

    def render_row(self, name, seconds):
        row = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=10)

        name_label = ctk.CTkLabel(
            row,
            text=name,
            font=("Segoe UI", 15, "bold"),
            anchor="w"
        )
        name_label.pack(side="left")

        time_label = ctk.CTkLabel(
            row,
            text=format_seconds(seconds),
            font=("Segoe UI", 15),
            anchor="e"
        )
        time_label.pack(side="right")


if __name__ == "__main__":
    init_db()
    app = Dashboard()
    app.mainloop()