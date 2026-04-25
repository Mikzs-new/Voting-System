# ui/login_window.py
import tkinter as tk

from api_client import APIClient
from logger_setup import LOGGER


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.api_client = APIClient()
        self.main_frame = None
        self.setup_ui()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("School Voting System - Staff Login")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

        self.main_frame = tk.Frame(self.root, padx=40, pady=40)
        self.main_frame.pack(fill='both', expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="School Voting System",
            font=("Arial", 18, "bold"),
            fg="#4CAF50"
        )
        title_label.pack(pady=(0, 20))

        subtitle_label = tk.Label(
            self.main_frame,
            text="Staff Desktop Application",
            font=("Arial", 12),
            fg="#666"
        )
        subtitle_label.pack(pady=(0, 30))

        tk.Label(self.main_frame, text="Username / Email:", font=("Arial", 10)).pack(anchor='w')
        self.username_entry = tk.Entry(self.main_frame, font=("Arial", 11), width=30)
        self.username_entry.pack(pady=(5, 15))

        tk.Label(self.main_frame, text="Password:", font=("Arial", 10)).pack(anchor='w')
        self.password_entry = tk.Entry(self.main_frame, show="*", font=("Arial", 11), width=30)
        self.password_entry.pack(pady=(5, 20))

        self.login_button = tk.Button(
            self.main_frame,
            text="LOGIN",
            command=self.login,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.login_button.pack()

        self.status_label = tk.Label(self.main_frame, text="", font=("Arial", 9), fg="red")
        self.status_label.pack(pady=(10, 0))

        self.root.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        self.login_button.config(state='disabled', text="Logging in...")
        self.status_label.config(text="")
        LOGGER.info("Desktop login screen accepted raw input user=%s", username or "Guest")

        success = self.api_client.guest_login(username, password)
        self._finish_login(success)

    def _finish_login(self, success):
        if success:
            self.on_login_success(self.api_client)
            return

        LOGGER.warning("Login rejected by backend")
        self.status_label.config(text="Unable to continue")
        self.login_button.config(state='normal', text="LOGIN")

    def destroy(self):
        if self.main_frame and self.main_frame.winfo_exists():
            self.main_frame.destroy()
