import json

clipboard_history_file = '/home/seva/Документы/projects/Python/clipboard/clipboard_history.json'

def load_history():
    try:
        with open(clipboard_history_file, 'r') as file:
            history = json.load(file)
        return history
    except FileNotFoundError:
        return []

def save_history(history):
    with open(clipboard_history_file, 'w') as file:
        json.dump(history, file)

def shorten_text(text, limit=50):
    return text if len(text) <= limit else text[:limit-3] + "..."

