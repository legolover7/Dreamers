import pygame as pyg

# Keyboard input for text boxes
def handler(content, key, key_mods, cursor):
    '''
    Edits the given content based on the key(s) pressed
    Parameters: The content to be edited, the event.key from pygame, the current keyboard mods, and the current cursor location
    Returns: The edited content and the adjusted cursor
    '''
    shift, caps, ctrl = key_mods
    if cursor > len(content):
        cursor = len(content)

    # Normal keys
    char = ""
    if 97 <= key <= 122:
        char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[key-97] if caps or shift else "abcdefghijklmnopqrstuvwxyz"[key-97]
        cursor += 1
    if 44 <= key <= 57:
        char = "<->?)!@#$%^&*("[key-44] if shift else ",_./0123456789"[key-44]
        cursor += 1

    if key == 39:
        char = "\"" if shift else "'"
        cursor += 1
    if key == 96:
        char = "~" if shift else "`"
        cursor += 1
    if key == 61:
        char = "+" if shift else "="
        cursor += 1
    if key == 59:
        char = ":" if shift else ";"
        cursor += 1
    if key == 91:
        char = "{" if shift else "["
        cursor += 1
    if key == 93:
        char = "}" if shift else "]"
        cursor += 1
    if key == pyg.K_SPACE:
        char = " " 
        cursor += 1
        
    content = content[:cursor-1] + char + content[cursor-1:]

    # Ctrl+Shift+Backspace == delete all content
    if key == pyg.K_BACKSPACE and ctrl and shift and len(content) > 0:
        content = ""
        cursor = 0
        return content, cursor

    # Ctrl/Backspace
    if key == pyg.K_BACKSPACE and len(content) > 0 and cursor != 0:
        if not ctrl:
            content = content[:cursor-1] + content[cursor:]
            cursor = max(cursor-1, 0)
        else:
            content += " " 
            for i in range(cursor, 0, -1):
                i -= 1
                if content[i] == " ":
                    break
            content = content[:i] + content[cursor:]
            cursor = i
            content = content[:-1]

    # Ctrl/Delete
    if key == pyg.K_DELETE and len(content) > 0 and cursor != len(content):
        if not ctrl:
            content = content[:cursor] + content[cursor+1:]
        else:
            for i in range(cursor, len(content)):
                if content[i] == " ":
                    break
            content = content[:cursor] + content[i+1:]

    # Left/right arrows
    if key == pyg.K_LEFT:
        if ctrl:
            j = cursor
            for i in range(cursor, 0, -1):
                    j -= 1
                    if content[j] == " ":
                        break
            cursor = j
        else:
            cursor = max(0, cursor - 1)
    elif key == pyg.K_RIGHT:
        if ctrl:
            j = cursor
            for j in range(cursor, len(content)):
                    if content[j] == " " and j != cursor:
                        break
            cursor = j
        else:
            cursor = min(cursor + 1, len(content))

    # Home/end keys
    elif key == pyg.K_HOME:
        cursor = 0
    elif key == pyg.K_END:
        cursor = len(content)

    return content, cursor
