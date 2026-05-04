"""
╔══════════════════════════════════════════════════════════════════╗
║  main.py  —  Entry Point for Jarvis Assistant                    ║
║  Run this file to start the assistant:  python main.py           ║
╚══════════════════════════════════════════════════════════════════╝

HOW THE PACKAGE WORKS (big picture)
────────────────────────────────────
  User speaks → listener module hears & parses → executor module acts

  main.py  ──imports──▶  jarvis_assistant (Package)
                               ├── listener  (Module 1)
                               │     ├── listen_for_command()   → str
                               │     ├── set_timeout()          → bool
                               │     ├── get_recognized_words() → list
                               │     ├── check_confidence()     → bool
                               │     └── parse_command()        → dict
                               └── executor  (Module 2)
                                     ├── open_application()     → bool
                                     ├── get_app_path()         → str
                                     ├── list_commands()        → list
                                     ├── speak_response()       → None
                                     └── execute_command()      → tuple
"""

# ── Import both modules from our package ─────────────────────────
import listener
import executor


def run_jarvis():
    """
    Main loop: listens for a command, parses it, then executes it.
    Runs until the user says 'exit', 'quit', or 'stop jarvis'.
    """
    print("\n" + "═" * 55)
    print("   J.A.R.V.I.S  —  Voice Assistant  |  1st Sem Project")
    print("═" * 55)
    print("  Say 'open chrome'  /  'open edge'  /  'open notepad'")
    print("  Say 'exit' or 'quit' to stop.")
    print("═" * 55 + "\n")

    # ── Step 1: Configure the listener ───────────────────────────
    listener.set_timeout(7)          # wait 7 seconds for voice (int → bool)
    executor.speak_response("Hello! I am Jarvis. How can I help you?")

    while True:
        # ── Step 2: Listen for voice input ───────────────────────
        raw_text: str = listener.listen_for_command()   # returns str

        # ── Step 3: Exit condition ───────────────────────────────
        if raw_text in ("exit", "quit", "stop jarvis", "goodbye"):
            executor.speak_response("Goodbye! Shutting down.")
            print("[JARVIS] Session ended.")
            break

        if raw_text == "":
            continue          # nothing heard, try again

        # ── Step 4: Extract words (for debugging / display) ──────
        words: list = listener.get_recognized_words(raw_text)   # list
        print(f"[MAIN] Words detected: {words}")

        # ── Step 5: Parse the sentence into action + target ──────
        command: dict = listener.parse_command(raw_text)        # dict
        print(f"[MAIN] Command parsed: {command}")

        # ── Step 6: Execute the command ──────────────────────────
        result: tuple = executor.execute_command(command)       # tuple
        success, message = result           # unpack tuple → (bool, str)
        print(f"[MAIN] Result → Success={success} | {message}\n")


# ── Only run when this file is executed directly ─────────────────
if __name__ == "__main__":
    run_jarvis()
