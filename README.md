# Coding-Stats

Coding Stats is a private, open-source desktop app that tracks your real coding time across VS Code, terminal, and other dev tools.
See daily/weekly trends, identify productive hours, and export your stats.

**No cloud, no tracking — just local insights to improve your workflow.**

---

## ✨ Features

* ⏱ Track time spent on developer tools (VS Code, Terminal, Browser, etc.)
* 📊 Daily statistics by category (Coding, Terminal, API Testing, etc.)
* 🧠 Language detection (Python, JavaScript, TypeScript…)
* 💻 Software usage breakdown
* ⚡ Lightweight background tracker
* 🔒 Fully local (SQLite database, no external services)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Chrisiisx/Coding-Stats
cd coding-stats
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Start the tracker

```bash
python -m app.tracker
```

---

### 5. Open the dashboard

```bash
python main.py
```

---

## 🧠 How it works

Coding Stats runs locally and:

1. Detects the **active window** every second
2. Identifies the **process (VS Code, Terminal, etc.)**
3. Classifies it into categories
4. Stores aggregated time in a local **SQLite database**
5. Extracts programming language from file names (e.g. `.py`, `.ts`)

All data is stored locally in:

```txt
codingstats.db
```

---

## ⚙️ Configuration

You can customize tracked apps and languages:

### `config/apps.json`

```json
{
  "Code.exe": {
    "display_name": "Visual Studio Code",
    "category": "Coding"
  }
}
```

---

### `config/languages.json`

```json
{
  ".py": "Python",
  ".js": "JavaScript"
}
```

---

## 📦 Project Structure

```txt
app/
├─ tracker.py
├─ dashboard.py
├─ database.py
├─ classifier.py
├─ language_detector.py

config/
├─ apps.json
├─ languages.json
```

---

## 🧪 Roadmap

* [ ] Shareable stats card (export as image)
* [ ] System tray integration
* [ ] Weekly/monthly reports
* [ ] Plugin system for custom apps
* [ ] Cross-platform support (macOS, Linux)

---

## 🤝 Contributing

Contributions are welcome.

### Ways to contribute:

* Add new app mappings in `apps.json`
* Improve language detection
* Add UI improvements
* Fix bugs / performance issues

### Setup for contributors

```bash
git fork
git clone your-fork
```

Create a new branch:

```bash
git checkout -b feature/your-feature
```

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🔒 Privacy

Coding Stats:

* ❌ does NOT collect personal data
* ❌ does NOT send data to any server
* ✅ stores everything locally

---

## ⭐ Support

If you find this project useful:

* star the repository
* share your stats
* contribute

---

Built for developers who want to understand how they actually spend their time.
