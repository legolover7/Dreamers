import sys

import editor.editor as editor

args = sys.argv[1:]

editor_names = ["editor", "e", "ed"]

if args[0].lower() in editor_names:
    editor.Main()