# Function that splits up a string, returning a list of chunks that are no more than the given max_length
def chunk(text, max_length=0, content_width=0, char_width=0):
    '''
    Chunks provided text into sub slices based on the max_length variable
    Parameters: The text to be chunked, an integer max_length to chop to a specific size, content_width and char_size which calculates into max_length
    Returns: A list with strings that are less than or equal to max_length in size
    '''
    if len(text) == 0:
        return []
    if content_width != 0 and char_width != 0:
        try:
            max_length = content_width // char_width
        except:
            return [text]
    
    
    begin_spc = False
    char = False
    if text[0] == " ":
        begin_spc = True
    text_list = []
    out_list = []

    tail = 0
    # Split text on spaces
    for head in range(len(text)):
        if text[head] == " " and char or head == len(text)-1:
            text_list += [text[tail:head+1]]
            tail = head
            char = False
        else:
            char = True
        
    # Consolidate spaces and remove preceding ones
    index = 0
    while index != len(text_list):
        if len(text_list[index]) > 0:
            if text_list[index] == " ":
                text_list[index-1] += " "
                text_list.pop(index)
                index -= 1
        if len(text_list[index]) > 1 and text_list[index][0] == " ":
            text_list[index] = text_list[index][1:]
        index += 1

    temp = (" " if begin_spc else "") + text_list.pop(0)

    if len(temp) > max_length:
        text_list.insert(0, temp[max_length:])
        temp = temp[:max_length]

    # Loop while list not empty
    while len(text_list) > 1:
        # Can fit both strings (add a space between)
        if len(temp + text_list[0] + text_list[1]) <= max_length:
            temp += text_list.pop(0)
        # Can only fit the current string (no space)
        elif len(temp + text_list[0]) <= max_length:
            temp += text_list.pop(0)
            out_list += [temp]
            temp = text_list.pop(0)
        # New line
        else:
            out_list += [temp]
            temp = text_list.pop(0)

    # Final formatting
    if len(text_list) > 0:
        if len(temp + text_list[0]) < max_length:
            temp += text_list[0]
            out_list += [temp]
        else:
            out_list += [temp]
            out_list += [text_list[0]]
    else:
        temp = temp
        while len(temp) > max_length:
            out_list += [temp[:max_length]]
            temp = temp[max_length:]
        out_list += [temp]

    return out_list

