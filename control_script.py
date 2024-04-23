import sys

args = sys.argv[1:]

editor_names = ["editor", "ed", "e"]
engine_names = ["search_engine", "se", "s"]

if len(args) == 0:
    print("Please enter a command! Available commands:")
    print("To open the editor:", editor_names, "To open the search engine:", engine_names)
    print("Correct usage: python control_script.py <command>")
    sys.exit()

import editor.editor as editor
import search_engine.search_engine as search_engine

if args[0].lower() in editor_names:
    editor.Main()

elif args[0].lower() in engine_names:
    search_engine.Main()

    