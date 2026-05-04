"""
╔══════════════════════════════════════════════════════════╗
║        JARVIS ASSISTANT — Python Package                 ║
║        Package Name  : jarvis_assistant                  ║
║        Modules       : listener  |  executor             ║
║        Purpose       : Voice-controlled desktop assistant║
╚══════════════════════════════════════════════════════════╝

WHAT IS A PACKAGE?

A Python Package is a folder that contains multiple modules
(i.e. .py files) grouped together under one name so they
can be imported and reused easily.

This file (__init__.py) tells Python:
  "Hey! This folder is a package, not just a folder."

When you write:
    from jarvis_assistant import listener
    from jarvis_assistant import executor
Python looks inside this folder because of __init__.py.
"""

# Make both modules accessible directly via the package
from . import listener
from . import executor

# Package metadata
__version__  = "1.0.0"
__author__   = "Swastik_Johan_Dev[25124(107.119.121)]"
__college__  = "Python Project"

print(f"[JARVIS] Package v{__version__} loaded. Modules ready: listener, executor")
