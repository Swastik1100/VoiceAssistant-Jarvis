# 🤖 Jarvis Assistant
> A Python voice assistant for your desktop — speak a command, watch it happen.
> College Project · Python Package Architecture

---

## 📌 Project Overview

Jarvis Assistant is a voice-controlled desktop assistant built entirely in Python. It listens to your microphone, understands what you said, and performs real actions like opening Chrome, Edge, Notepad, or the Calculator — then speaks back a confirmation.

The project is structured as a **Python Package** containing two **Modules**, each with multiple **Functions** — demonstrating core Python concepts: packages, modules, functions, and data types (`str`, `int`, `float`, `bool`, `list`, `dict`, `tuple`, `None`).

---

## 🗂️ Project Structure

```
jarvis_assistant/         ← Package (folder with __init__.py)
│
├── __init__.py           ← Makes this folder a Python package
├── listener.py           ← Module 1: captures & parses voice input
└── executor.py           ← Module 2: executes actions & speaks responses

main.py                   ← Entry point — run this to start Jarvis
requirements.txt          ← Required third-party libraries
README.md                 ← This file
```

---

## ⚙️ How It Works

```
You speak  →  listener hears  →  listener parses  →  executor acts  →  Jarvis confirms
  "open         str returned      dict returned        bool returned     speaks aloud
   chrome"
```

1. `listener.listen_for_command()` opens the mic and returns your spoken words as a `str`
2. `listener.parse_command()` converts that string into a structured `dict` like `{"action": "open", "target": "chrome"}`
3. `executor.execute_command()` reads the dict, launches the app, and returns a `tuple` result
4. `executor.speak_response()` confirms the action aloud via text-to-speech

---

## 📦 Requirements

**Python version:** 3.8 or higher

**Install dependencies:**
```bash
pip install -r requirements.txt
```

| Library | Version | Purpose |
|---|---|---|
| `SpeechRecognition` | 3.10.4 | Converts microphone audio to text |
| `pyttsx3` | 2.90 | Offline text-to-speech (Jarvis speaks back) |
| `PyAudio` | 0.2.14 | Microphone access (required by SpeechRecognition) |



## ▶️ Running the Project

```bash
python main.py
```

Jarvis will greet you and start listening. Speak one of the supported commands below.

---

## 🎙️ Supported Voice Commands


| `open chrome` | Launches Google Chrome |
| `open edge` | Launches Microsoft Edge |
| `open notepad` | Opens Notepad / text editor |
| `open calculator` | Opens the Calculator |
| `open file explorer` | Opens File Explorer |
| `open vs code` | Launches Visual Studio Code |
| `exit` / `quit` / `goodbye` | Stops Jarvis |

You can also use aliases — `"google chrome"`, `"google"`, `"browser"` all open Chrome.

---

## 🧩 Module Reference

### Module 1 — `listener.py`
**Sub-goal:** Hear and understand the user's voice

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `listen_for_command()` | — | `str` | Opens mic, returns recognised speech as lowercase text |
| `set_timeout(seconds)` | `int` | `bool` | Sets how many seconds to wait for voice input |
| `get_recognized_words(text)` | `str` | `list` | Splits sentence into individual words |
| `check_confidence(score)` | `float` | `bool` | Returns `True` if score ≥ 0.70, else `False` |
| `parse_command(text)` | `str` | `dict` | Extracts `{"action": ..., "target": ..., "raw": ...}` |

**Example:**
```python
from jarvis_assistant import listener

text = listener.listen_for_command()        # "open chrome"
words = listener.get_recognized_words(text) # ["open", "chrome"]
cmd   = listener.parse_command(text)        # {"action": "open", "target": "chrome", "raw": "open chrome"}
```

---

### Module 2 — `executor.py`
**Sub-goal:** Execute actions and respond to the user

| Function | Parameters | Returns | Description |
|---|---|---|---|
| `open_application(app_name)` | `str` | `bool` | Launches a registered desktop application |
| `get_app_path(app_name)` | `str` | `str` | Returns the OS-specific executable path |
| `list_commands()` | — | `list` | Lists all app names Jarvis can open |
| `speak_response(message)` | `str` | `None` | Speaks a sentence aloud via text-to-speech |
| `execute_command(command)` | `dict` | `tuple` | Dispatches the parsed command; returns `(bool, str)` |

**Example:**
```python
from jarvis_assistant import executor

apps   = executor.list_commands()                          # ["chrome", "edge", ...]
result = executor.execute_command({"action": "open",
                                   "target": "chrome",
                                   "raw":    "open chrome"})
# result → (True, "Opened chrome successfully")
success, message = result
```

---

## 🧠 Key Python Concepts Demonstrated

| Concept | Where used | Example |
|---|---|---|
| **Package** | `jarvis_assistant/` folder | `from jarvis_assistant import listener` |
| **Module** | `listener.py`, `executor.py` | Two `.py` files, one per sub-goal |
| **Function** | Every `.py` file | `def parse_command(text): ...` |
| **`str`** | Spoken text, app names | `"open chrome"` |
| **`int`** | Timeout in seconds | `set_timeout(7)` |
| **`float`** | Confidence score | `check_confidence(0.93)` |
| **`bool`** | Success / failure flags | `True` / `False` |
| **`list`** | Word lists, app lists | `["open", "chrome"]` |
| **`dict`** | Parsed command structure | `{"action": "open", "target": "chrome"}` |
| **`tuple`** | Execute result pair | `(True, "Opened chrome successfully")` |
| **`None`** | TTS function return | `speak_response()` returns `None` |

---

