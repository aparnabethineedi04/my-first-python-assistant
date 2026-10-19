
# Tools for MyFirstAIAgent

from pathlib import Path

NOTES_FILE = Path(__file__).with_name("notes.txt")


def greet(name):
    return "Hello, " + name + "! Welcome back."


def learn_about_ai():
    return (
        "AI means Artificial Intelligence. "
        "It helps computers perform tasks that usually "
        "require human intelligence."
    )


def add_numbers(first, second):
    return first + second


def remember_note(note):
    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(note + "\n")

    return "Your note has been saved."


def get_notes():
    if not NOTES_FILE.exists():
        return []

    with NOTES_FILE.open("r", encoding="utf-8") as file:
        return [
            line.rstrip("\n")
            for line in file
            if line.rstrip("\n")
        ]

def search_notes(keyword):
    notes = get_notes()
    keyword = keyword.strip().lower()

    if not keyword:
        return ["Please provide a keyword to search."]

    matches = [
        note for note in notes
        if keyword in note.lower()
    ]

    if matches:
        return matches

    return ["No matching notes were found."]
