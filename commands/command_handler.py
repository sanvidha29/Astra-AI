from commands.system_commands import *
from commands.web_commands import *

COMMANDS = {

    "open chrome": open_chrome,

    "open youtube": open_youtube,

    "open gmail": open_gmail,

    "open github": open_github,

    "open calculator": open_calculator,

    "open notepad": open_notepad,

    "open explorer": open_file_explorer,

    "open file explorer": open_file_explorer,

    "open vs code": open_vscode,
    "open spotify": open_spotify,

}


def execute_command(command):

    command = command.lower()

    for keyword, function in COMMANDS.items():

        if keyword in command:

            return function()

    return None