import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from functions import load_history, save_history, shorten_text

class ClipboardHistoryWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="История буфера обмена")
        self.set_default_size(400, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)
        notebook = Gtk.Notebook()
        vbox.pack_start(notebook, True, True, 0)
        self.init_pages(notebook)
        self.add_clear_button(vbox, notebook)
        self.update_ui(notebook)

    def init_pages(self, notebook):
        # Все элементы
        all_scrollable_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        all_scrolled_window = Gtk.ScrolledWindow()
        all_scrolled_window.set_hexpand(True)
        all_scrolled_window.set_vexpand(True)
        all_scrolled_window.add(all_scrollable_box)
        notebook.append_page(all_scrolled_window, Gtk.Label(label='Все'))

        # Избранные элементы
        fav_scrollable_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        fav_scrolled_window = Gtk.ScrolledWindow()
        fav_scrolled_window.set_hexpand(True)
        fav_scrolled_window.set_vexpand(True)
        fav_scrolled_window.add(fav_scrollable_box)
        notebook.append_page(fav_scrolled_window, Gtk.Label(label='Избранные'))

    def add_clear_button(self, vbox, notebook):
        clear_button = Gtk.Button(label="Очистить историю и буфер обмена")
        clear_button.connect("clicked", self.clear_clipboard_history, notebook)
        vbox.pack_start(clear_button, False, False, 0)

    def update_ui(self, notebook):
        clipboard_history = load_history()
        clipboard_history = reversed(clipboard_history)  # Инвертируем порядок списка
        
        all_page = notebook.get_nth_page(0).get_child()
        fav_page = notebook.get_nth_page(1).get_child()

        # Очищаем содержимое страниц
        for child in all_page.get_children():
            all_page.remove(child)
        for child in fav_page.get_children():
            fav_page.remove(child)

        # Добавляем элементы в соответствующие страницы
        for item in clipboard_history:
            hbox = Gtk.Box(spacing=6)
            button_text = shorten_text(item["text"])
            button = Gtk.Button(label=button_text)
            button.connect("clicked", self.copy_to_clipboard, item["text"])
            hbox.pack_start(button, True, True, 0)

            
            favorite_button = Gtk.ToggleButton()
            favorite_button.set_label("☆" if not item.get("favorite", False) else "★")
            favorite_button.set_active(item.get("favorite", False))
            favorite_button.connect("toggled", self.toggle_favorite, item["text"])
            hbox.pack_start(favorite_button, False, False, 0)

            if item.get("favorite", False):
                fav_page.add(hbox)
            else:
                all_page.add(hbox)

        notebook.show_all()

    def toggle_favorite(self, button, item_text):
        history = load_history()
        for item in history:
            if item["text"] == item_text:
                item["favorite"] = not item.get("favorite", False)
                break
        save_history(history)
        self.update_ui(button.get_parent().get_parent())

    def clear_clipboard_history(self, button, notebook):
        save_history([])
        self.update_ui(notebook)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.clear()

    def copy_to_clipboard(self, button, text):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)

def main():
    win = ClipboardHistoryWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

