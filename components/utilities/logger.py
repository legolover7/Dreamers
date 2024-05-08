import time

class WarningLevels:
    INFO = 0
    WARN = 1
    ERROR = 2

    messages = [
        "\u001b[37m" + "[INFO]" + "\u001b[0m",
        "\u001b[33m" + "[WARNING]" + "\u001b[0m",
        "\u001b[31m" + "[ERROR]" + "\u001b[0m"
    ]
    

def MarkLog(level, message):
    current_time = time.strftime("%m/%d/%Y [%I:%M:%S]")

    warn_level = WarningLevels.messages[level] + ":"

    print(current_time, warn_level, message)

def WriteLog(level, message, filename):
    current_time = time.strftime("%m/%d/%Y [%I:%M:%S]")

    warn_level = ["[INFO]", "[WARNING]", "[ERROR]"][level] + ":"

    with open(filename, "a") as outfile:
        message = current_time + " " + warn_level + " " + message + "\n"
        outfile.write(message)