import pyperclip
import json
import time

clipboard_history_file = '/home/seva/Документы/projects/Python/clipboard/clipboard_history.json'

def load_history():
    try:
        with open(clipboard_history_file, 'r') as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []
    return history

def save_history(content):
    history = load_history()
    
    # Проверяем, есть ли уже такой текст в истории
    if not any(item["text"] == content for item in history):
        # Если нет, добавляем его как новый элемент
        history.append({"text": content, "favorite": False})
        with open(clipboard_history_file, 'w') as file:
            json.dump(history, file, indent=4, ensure_ascii=False)

last_clipboard_content = pyperclip.paste()

while True:
    try:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != last_clipboard_content:
            print("Обнаружено новое содержимое буфера обмена. Сохранение...")
            save_history(current_clipboard_content)
            last_clipboard_content = current_clipboard_content
    except Exception as e:
    	print(f"Произошла ошибка: {type(e).__name__}: {e}")
    time.sleep(1)

