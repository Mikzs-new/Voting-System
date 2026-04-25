import tkinter as tk

from logger_setup import LOGGER
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


class VotingDesktopApp:
    """Backward-compatible launcher that uses the active API-backed desktop app."""

    def __init__(self, root):
        self.root = root
        self.current_window = None
        self.show_login()

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, api_client):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = MainWindow(self.root, api_client)


if __name__ == "__main__":
    LOGGER.info("Legacy launcher started; redirecting to API-backed desktop app")
    root = tk.Tk()
    app = VotingDesktopApp(root)
    root.mainloop()
