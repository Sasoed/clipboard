import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class StartupDialog(Gtk.MessageDialog):
    def __init__(self):
        super().__init__(flags=0, message_type=Gtk.MessageType.INFO,
                         buttons=Gtk.ButtonsType.OK, text="Всплывающее окно при запуске")
        self.set_default_size(300, 100)
        self.format_secondary_text(
            "Это окно появляется сразу при запуске программы.")
        self.connect("response", self.on_response)

    def on_response(self, widget, response_id):
        # Закрываем диалог при любом ответе
        self.destroy()

def main():
    dialog = StartupDialog()
    dialog.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()

