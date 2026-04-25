#!/usr/bin/env python
# main.py - Main entry point for the desktop application

import sys
import tkinter as tk
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from logger_setup import LOGGER

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.current_window = None
    
    def run(self):
        self.show_login()
        self.root.mainloop()
    
    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginWindow(self.root, self.on_login_success)
    
    def on_login_success(self, api_client):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = MainWindow(self.root, api_client)

if __name__ == "__main__":
    LOGGER.info("Desktop application starting")
    app = Application()
    app.run()
