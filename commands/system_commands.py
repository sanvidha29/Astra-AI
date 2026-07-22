import subprocess


def open_calculator():
    subprocess.Popen("calc")
    return "Opening Calculator."


def open_notepad():
    subprocess.Popen("notepad")
    return "Opening Notepad."


def open_file_explorer():
    subprocess.Popen("explorer")
    return "Opening File Explorer."


def open_vscode():
    subprocess.Popen("code")
    return "Opening VS Code."