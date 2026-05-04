"""
╔══════════════════════════════════════════════════════════════════╗
║  MODULE 1 : listener.py                                          ║
║  Role     : Captures and processes user's voice input            ║
║  Sub-goal : "Hear and understand what the user said"             ║
╚══════════════════════════════════════════════════════════════════╝

WHAT IS A MODULE?
-----------------
A module is a single Python file (.py) that contains related
functions, variables, and logic grouped for one specific purpose.

This module handles everything about LISTENING:
  - Capturing microphone input
  - Converting speech to text
  - Validating and cleaning the text
  - Extracting keywords from spoken sentences

DATA TYPES USED IN THIS MODULE
-------------------------------
  str   → The recognised spoken text        e.g. "open chrome"
  int   → Timeout duration in seconds       e.g. 5
  float → Confidence score of recognition   e.g. 0.93
  bool  → True/False check on wake word     e.g. True
  list  → List of keywords extracted        e.g. ["open", "chrome"]
  dict  → Full parsed command structure     e.g. {"action": "open", "target": "chrome"}
"""

import speech_recognition as sr

# ── Shared recogniser instance used by all functions ─────────────
recogniser = sr.Recognizer()

# ── Configurable timeout (default: 5 seconds) ────────────────────
_timeout_seconds: int = 5


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 1  |  listen_for_command()
# Return type : str
# Purpose     : Opens the microphone and returns the recognised text.
# ═══════════════════════════════════════════════════════════════════
def listen_for_command() -> str:
    """
    Listens to the microphone and converts speech to a lowercase string.

    DATA TYPE USED: str
      - The recognised audio is converted to a str so the rest of the
        program can work with plain text.

    Returns:
        str : The spoken sentence in lowercase,
              OR an empty string "" if nothing was heard.

    Example:
        >>> command = listen_for_command()
        # User says "Open Chrome"
        >>> print(command)          # output: "open chrome"
        >>> type(command)           # output: <class 'str'>
    """
    print("[LISTENER] Listening… speak now.")
    try:
        with sr.Microphone() as mic:
            recogniser.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recogniser.listen(mic, timeout=_timeout_seconds)
            text: str = recogniser.recognize_google(audio)
            text = text.lower().strip()          # always lowercase → easier matching
            print(f"[LISTENER] Heard: '{text}'")
            return text
    except sr.WaitTimeoutError:
        print("[LISTENER] No speech detected within timeout.")
        return ""
    except sr.UnknownValueError:
        print("[LISTENER] Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"[LISTENER] API error: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 2  |  set_timeout(seconds)
# Param type  : int
# Return type : bool
# Purpose     : Lets you change how long Jarvis waits for your voice.
# ═══════════════════════════════════════════════════════════════════
def set_timeout(seconds: int) -> bool:
    """
    Sets the microphone listening timeout in whole seconds.

    DATA TYPES USED:
      - int  : 'seconds' must be a whole number (e.g. 5, not 5.5).
      - bool : Returns True if the value was accepted, False otherwise.

    Args:
        seconds (int): How many seconds to wait for voice. Must be 1–30.

    Returns:
        bool : True  → timeout updated successfully.
               False → invalid value provided.

    Example:
        >>> result = set_timeout(10)
        >>> print(result)           # output: True
        >>> type(result)            # output: <class 'bool'>

        >>> result = set_timeout(0)
        >>> print(result)           # output: False  (0 is not valid)
    """
    global _timeout_seconds
    if isinstance(seconds, int) and 1 <= seconds <= 30:
        _timeout_seconds = seconds
        print(f"[LISTENER] Timeout set to {seconds} second(s).")
        return True
    else:
        print(f"[LISTENER] Invalid timeout: {seconds}. Must be int between 1 and 30.")
        return False


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 3  |  get_recognized_words(text)
# Param type  : str
# Return type : list
# Purpose     : Splits the spoken sentence into individual words.
# ═══════════════════════════════════════════════════════════════════
def get_recognized_words(text: str) -> list:
    """
    Splits a recognised sentence into a list of individual words.

    DATA TYPES USED:
      - str  : Input is the full spoken sentence.
      - list : Output is each word as a separate item in a list.

    Args:
        text (str): The full recognised sentence e.g. "open chrome browser".

    Returns:
        list : Each word as a string inside a list.
               e.g. ["open", "chrome", "browser"]
               Returns [] if text is empty.

    Example:
        >>> words = get_recognized_words("open chrome browser")
        >>> print(words)            # output: ['open', 'chrome', 'browser']
        >>> type(words)             # output: <class 'list'>
        >>> print(len(words))       # output: 3
    """
    if not text or not isinstance(text, str):
        return []
    words: list = text.strip().split()
    print(f"[LISTENER] Words extracted: {words}")
    return words


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 4  |  check_confidence(score)
# Param type  : float
# Return type : bool
# Purpose     : Decides if a recognition confidence score is good enough.
# ═══════════════════════════════════════════════════════════════════
def check_confidence(score: float) -> bool:
    """
    Checks whether the speech recognition confidence is above the threshold.

    DATA TYPES USED:
      - float : Confidence is a decimal number between 0.0 (0%) and 1.0 (100%).
      - bool  : Returns True if confidence is acceptable, False if too low.

    The threshold is set at 0.70 (70%). Below that, we ignore the input.

    Args:
        score (float): Confidence value from the recognition engine.

    Returns:
        bool : True  → confidence is good; proceed with command.
               False → confidence is too low; ask user to repeat.

    Example:
        >>> check_confidence(0.93)  # output: True   (93% confident ✔)
        >>> check_confidence(0.45)  # output: False  (45% too low ✘)
        >>> type(0.93)              # output: <class 'float'>
    """
    THRESHOLD: float = 0.70
    result: bool = isinstance(score, float) and score >= THRESHOLD
    if result:
        print(f"[LISTENER] Confidence {score:.0%} — accepted ✔")
    else:
        print(f"[LISTENER] Confidence {score:.0%} — too low, ignored ✘")
    return result


# ═══════════════════════════════════════════════════════════════════
# FUNCTION 5  |  parse_command(text)
# Param type  : str
# Return type : dict
# Purpose     : Converts a raw sentence into a structured command dictionary.
# ═══════════════════════════════════════════════════════════════════
def parse_command(text: str) -> dict:
    """
    Parses a raw sentence and returns a structured command as a dictionary.

    DATA TYPES USED:
      - str  : Input is the raw sentence from the microphone.
      - dict : Output maps "action" and "target" keys to their values.

    A dict (dictionary) is like a labelled box:
      {"action": "open", "target": "chrome"}
       action → what to do    target → what to do it to

    Args:
        text (str): The full sentence e.g. "open chrome" or "close edge".

    Returns:
        dict : {"action": str, "target": str, "raw": str}
               OR {"action": "unknown", "target": "", "raw": text}

    Example:
        >>> cmd = parse_command("open chrome")
        >>> print(cmd)
        # output: {'action': 'open', 'target': 'chrome', 'raw': 'open chrome'}
        >>> type(cmd)               # output: <class 'dict'>
        >>> print(cmd["action"])    # output: 'open'
        >>> print(cmd["target"])    # output: 'chrome'
    """
    ACTION_WORDS = {"open", "close", "launch", "start", "stop", "search", "play"}
    words: list = get_recognized_words(text)

    command: dict = {"action": "unknown", "target": "", "raw": text}

    for i, word in enumerate(words):
        if word in ACTION_WORDS:
            command["action"] = word
            # Everything after the action word is the target
            command["target"] = " ".join(words[i + 1:])
            break

    print(f"[LISTENER] Parsed command: {command}")
    return command
