"""
╔══════════════════════════════════════════════════════════════════╗
║  MODULE 2 : executor.py                                          ║
║  Role     : Executes actions based on the parsed voice command   ║
║  Sub-goal : "Act on what the user asked for"                     ║
╚══════════════════════════════════════════════════════════════════╝

WHAT IS A MODULE?
-----------------
Just like listener.py handles the "hearing" part, this module
handles the "doing" part — it takes the parsed command and performs
real actions: opening browsers, speaking back, listing options, etc.

DATA TYPES USED IN THIS MODULE
-------------------------------
  str   → Application name / spoken response   e.g. "chrome"
  bool  → Did the app open successfully?       e.g. True
  list  → All supported command names          e.g. ["chrome", "edge", ...]
  dict  → App details (name, path, aliases)    e.g. {"path": "...", "aliases": [...]}
  tuple → (success: bool, message: str) result e.g. (True, "Opened chrome")
  None  → speak_response returns nothing       (it just plays audio)
"""

import subprocess #It allows Python to step outside of its own process and run programs or commands directly on your computer's operating system.
import platform  #To make your code "cross-platform" (working on Windows, Mac, and Linux)
import pyttsx3  #Offline TTS

# ── Text-to-speech engine (shared across functions) ───────────────
_tts_engine = pyttsx3.init()
_tts_engine.setProperty("rate", 170)      # speaking speed (words per minute)
_tts_engine.setProperty("volume", 0.9)    # volume  0.0 → 1.0

# ── App registry: maps common names → OS-specific launch commands ─
#    Works on Windows. Adjust paths for Linux/macOS if needed.
_APP_REGISTRY: dict = {
    "chrome": {
        "windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "linux"  : "google-chrome",
        "darwin" : "open -a 'Google Chrome'",
        "aliases": ["google chrome", "google", "browser"],
    },
    "edge": {
        "windows": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "linux"  : "microsoft-edge",
        "darwin" : "open -a 'Microsoft Edge'",
        "aliases": ["microsoft edge", "ms edge"],
    },
    "notepad": {
        "windows": "notepad.exe",
        "linux"  : "gedit",
        "darwin" : "open -a TextEdit",
        "aliases": ["text editor", "notes"],
    },
    "calculator": {
        "windows": "calc.exe",
        "linux"  : "gnome-calculator",
        "darwin" : "open -a Calculator",
        "aliases": ["calc"],
    },
    "file explorer": {
        "windows": "explorer.exe",
        "linux"  : "nautilus",
        "darwin" : "open .",
        "aliases": ["explorer", "files", "my computer"],
    },
    "vs code": {
        "windows": "code",
        "linux"  : "code",
        "darwin" : "code",
        "aliases": ["visual studio code", "vscode", "code editor"],
    },
}


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 1  |  open_application(app_name)
# Param type  : str
# Return type : bool
# Purpose     : Opens a desktop application by name.
# ═══════════════════════════════════════════════════════════════════
def open_application(app_name: str) -> bool:
    """
    Launches a desktop application matching the given name.

    DATA TYPES USED:
      - str  : app_name is text e.g. "chrome", "notepad".
      - bool : Returns True if app launched OK, False on failure.

    Internally calls get_app_path() to find the correct OS path,
    then uses subprocess to launch the application.

    Args:
        app_name (str): The name of the app to open (case-insensitive).

    Returns:
        bool : True  → application opened successfully.
               False → app not found or launch failed.

    Example:
        >>> result = open_application("chrome")
        >>> print(result)           # output: True
        >>> type(result)            # output: <class 'bool'>

        >>> result = open_application("photoshop")
        >>> print(result)           # output: False  (not in registry)
    """
    app_name = app_name.lower().strip()
    path: str = get_app_path(app_name)

    if path == "":
        speak_response(f"Sorry, I don't know how to open {app_name}.")
        return False

    try:
        subprocess.Popen(path, shell=True)
        speak_response(f"Opening {app_name}.")
        print(f"[EXECUTOR] Launched: {path}")
        return True
    except Exception as e:
        print(f"[EXECUTOR] Failed to open '{app_name}': {e}")
        speak_response(f"Could not open {app_name}.")
        return False


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 2  |  get_app_path(app_name)
# Param type  : str
# Return type : str
# Purpose     : Returns the OS-specific launch command for an app.
# ═══════════════════════════════════════════════════════════════════
def get_app_path(app_name: str) -> str:
    """
    Looks up the system path / launch command for a known application.

    DATA TYPES USED:
      - str (input)  : The application name to look up.
      - str (output) : The OS-appropriate path/command string.
                       Returns "" (empty string) if not found.

    It also checks aliases so "google chrome" → finds "chrome" entry.

    Args:
        app_name (str): Name or alias of the app.

    Returns:
        str : The executable path or shell command for the current OS,
              or "" if the app is unknown.

    Example:
        >>> path = get_app_path("chrome")
        >>> print(path)
        # Windows → r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # Linux   → "google-chrome"
        >>> type(path)              # output: <class 'str'>

        >>> get_app_path("unknown_app")
        # output: ""   (empty string)
    """
    os_name: str = platform.system().lower()   # 'windows', 'linux', 'darwin'
    app_name = app_name.lower().strip()

    # Direct name match
    if app_name in _APP_REGISTRY:
        return _APP_REGISTRY[app_name].get(os_name, "")

    # Alias match  (e.g. "google chrome" → "chrome")
    for key, info in _APP_REGISTRY.items():
        if app_name in info.get("aliases", []):
            return _APP_REGISTRY[key].get(os_name, "")

    return ""          # not found → empty string


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 3  |  list_commands()
# Return type : list
# Purpose     : Returns all application names Jarvis can open.
# ═══════════════════════════════════════════════════════════════════
def list_commands() -> list:
    """
    Returns a list of all application names Jarvis knows how to open.

    DATA TYPE USED:
      - list : Each item in the list is a str (application name).
               e.g. ["chrome", "edge", "notepad", "calculator", ...]

    A list is an ordered, changeable collection:
      ["chrome", "edge", "notepad"]
       index 0    index 1   index 2

    Args:
        None

    Returns:
        list : All registered application name strings.

    Example:
        >>> apps = list_commands()
        >>> print(apps)
        # output: ['chrome', 'edge', 'notepad', 'calculator', 'file explorer', 'vs code']
        >>> type(apps)              # output: <class 'list'>
        >>> print(apps[0])          # output: 'chrome'
        >>> print(len(apps))        # output: 6
    """
    commands: list = list(_APP_REGISTRY.keys())
    print(f"[EXECUTOR] Available commands: {commands}")
    return commands


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 4  |  speak_response(message)
# Param type  : str
# Return type : None
# Purpose     : Makes Jarvis speak a sentence aloud.
# ═══════════════════════════════════════════════════════════════════
def speak_response(message: str) -> None:
    """
    Uses text-to-speech to say a message aloud — just like Jarvis/Siri.

    DATA TYPES USED:
      - str  : The message text to speak.
      - None : This function performs an action (speaking) and returns nothing.

    In Python, when a function returns nothing, its return type is None.
    Think of it like "void" in other languages.

    Args:
        message (str): The sentence Jarvis will speak.

    Returns:
        None

    Example:
        >>> speak_response("Opening Chrome now.")
        # [Jarvis says "Opening Chrome now." out loud via speakers]
        >>> result = speak_response("Hello!")
        >>> print(result)           # output: None
        >>> type(result)            # output: <class 'NoneType'>
    """
    print(f"[JARVIS SAYS] {message}")
    _tts_engine.say(message)
    _tts_engine.runAndWait()
    return None


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 5  |  execute_command(command)
# Param type  : dict
# Return type : tuple
# Purpose     : Takes a parsed command dict and executes the right action.
# ═══════════════════════════════════════════════════════════════════
def execute_command(command: dict) -> tuple:
    """
    The master dispatcher — takes a parsed command dictionary and
    calls the correct function to act on it.

    DATA TYPES USED:
      - dict  : Input is the structured command from listener.parse_command().
                e.g. {"action": "open", "target": "chrome", "raw": "open chrome"}
      - tuple : Output is a pair (bool, str) — success status + feedback message.
                e.g. (True, "Opened chrome successfully")

    A tuple is like a list but IMMUTABLE (cannot be changed after creation):
      (True, "Opened chrome")
       item0  item1

    Args:
        command (dict): Must have keys "action" and "target".

    Returns:
        tuple : (bool, str) → (was it successful?, what happened?)

    Example:
        >>> cmd = {"action": "open", "target": "chrome", "raw": "open chrome"}
        >>> result = execute_command(cmd)
        >>> print(result)           # output: (True, 'Opened chrome successfully')
        >>> type(result)            # output: <class 'tuple'>
        >>> success, msg = result   # unpack the tuple
        >>> print(success)          # output: True
        >>> print(msg)              # output: 'Opened chrome successfully'
    """
    action: str = command.get("action", "unknown")
    target: str = command.get("target", "")

    if action in ("open", "launch", "start"):
        success: bool = open_application(target)
        msg: str = f"Opened {target} successfully" if success else f"Failed to open {target}"
        return (success, msg)

    elif action in ("close", "stop"):
        speak_response(f"Close functionality for {target} is coming soon.")
        return (False, f"Close {target} — not yet implemented")

    elif action == "list":
        apps = list_commands()
        speak_response(f"I can open: {', '.join(apps)}")
        return (True, f"Listed {len(apps)} applications")

    else:
        speak_response("Sorry, I didn't understand that command.")
        return (False, f"Unknown action: {action}")
