import sys
import os

from search_engine.modules.save_handler import FilePaths

# Get arguments
args = sys.argv[1:]

editor_names = ["editor", "ed", "e"]
engine_names = ["search_engine", "se", "s"]

if len(args) == 0:
    print("Please enter a command! Available commands:")
    print("To open the editor:", editor_names, "To open the search engine:", engine_names)
    print("Correct usage: python control_script.py <arguments> <command>")
    sys.exit()

import editor.editor as editor
import search_engine.search_engine as search_engine

# Check arguments
if "-h" in args:
    print("Help menu")
    
# "Reset" argument
elif "-r" in args or "-rf" in args or "-fr" in args:
    print("Deleting Logs")
    if os.path.isfile(FilePaths.logs):
        os.remove(FilePaths.logs)
    print("Deleting Settings")
    if os.path.isfile(FilePaths.settings):
        os.remove(FilePaths.settings)

    # "Force" deletion (remove all data)
    if "-rf" in args or "-fr" in args:
        print("Deleting search terms")
        if os.path.isfile(FilePaths.terms):
            os.remove(FilePaths.terms)

if args[0].lower() in editor_names:
    editor.Main()

elif args[0].lower() in engine_names:
    search_engine.Main()

    